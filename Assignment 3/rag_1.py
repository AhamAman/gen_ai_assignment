from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_qdrant import QdrantVectorStore
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import streamlit as st
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
QDRANT_URL     = "http://localhost:6333"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ── Init embedder & LLM ───────────────────────────────────────────────────────
@st.cache_resource
def get_embedder():
    return GoogleGenerativeAIEmbeddings(
        google_api_key=GEMINI_API_KEY,
        model="models/text-embedding-004"
    )

@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GEMINI_API_KEY
    )

# ── Ingest uploaded PDF ───────────────────────────────────────────────────────
def ingest_pdf(uploaded_file) -> tuple[QdrantVectorStore, int, str]:
    """Save uploaded file to temp path, chunk it, embed it, store in Qdrant."""
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        # Load & split
        loader     = PyPDFLoader(file_path=tmp_path)
        docs       = loader.load()
        splitter   = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        split_docs = splitter.split_documents(docs)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)  # Always clean up temp file safely

    # Clean collection name for Qdrant compatibility
    collection_name = uploaded_file.name.replace(".pdf", "").replace(" ", "_").lower()

    # Embed & store
    vector_store = QdrantVectorStore.from_documents(
        documents=split_docs,
        url=QDRANT_URL,
        collection_name=collection_name,
        embedding=get_embedder(),
        force_recreate=True,
    )

    return vector_store, len(split_docs), collection_name

# ── RAG: retrieve + answer ────────────────────────────────────────────────────
def ask(question: str, chat_history: list, vector_store: QdrantVectorStore) -> tuple[str, list]:
    """Return (answer, source_chunks)."""

    results = vector_store.similarity_search(query=question, k=4)
    context = "\n\n".join([doc.page_content for doc in results])

    system_prompt = f"""You are a helpful AI study assistant. Answer the user's 
question using ONLY the context provided below. Be clear and concise.
If the answer is not in the context, say "I don't have enough information to answer that from this document."

Context:
{context}
"""

    messages = [SystemMessage(content=system_prompt)]
    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    messages.append(HumanMessage(content=question))

    response = get_llm().invoke(messages)

    # FIXED: Safe pagination fallback mapping
    sources = []
    for doc in results:
        raw_page = doc.metadata.get("page")
        page_num = int(raw_page) + 1 if raw_page is not None else "Unknown"
        sources.append({
            "page": page_num,
            "snippet": doc.page_content[:200] + "..."
        })

    return response.content, sources

# ── Streamlit UI ──────────────────────────────────────────────────────────────
def main():
    st.set_page_config(page_title="📚 PDF Study Assistant", page_icon="📚", layout="wide")
    st.title("📚 PDF Study Assistant")
    st.caption("Upload any PDF and ask questions about it")

    # Baseline Session State Initialization (Keep at top of main)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show_sources" not in st.session_state:
        st.session_state.show_sources = True

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.header("📂 Upload Document")
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

        if uploaded_file:
            if st.session_state.get("loaded_file") != uploaded_file.name:
                with st.spinner(f"Reading and indexing **{uploaded_file.name}**..."):
                    try:
                        vector_store, chunk_count, collection = ingest_pdf(uploaded_file)
                        st.session_state.vector_store  = vector_store
                        st.session_state.loaded_file   = uploaded_file.name
                        st.session_state.messages      = [] # Clear history on new file
                        st.session_state.collection    = collection
                        st.success(f"✅ Indexed **{chunk_count}** chunks!")
                    except Exception as e:
                        st.error(f"Error ingesting PDF: {e}")
            else:
                st.success(f"✅ `{uploaded_file.name}` loaded")

        st.markdown("---")
        st.session_state.show_sources = st.toggle("Show source passages", value=st.session_state.show_sources)

        st.markdown("---")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    # ── Main Chat Area ────────────────────────────────────────────────────────
    if "vector_store" not in st.session_state:
        st.info("👈 Upload a PDF from the sidebar to get started")
        return

    # Display historical conversation
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("sources") and st.session_state.show_sources:
                with st.expander("📄 Source passages used"):
                    for src in msg["sources"]:
                        st.markdown(f"**Page {src['page']}**")
                        st.caption(src["snippet"])
                        st.divider()

    # Handle incoming input
    if question := st.chat_input(f"Ask anything about {st.session_state.get('loaded_file')}..."):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching document and thinking..."):
                answer, sources = ask(
                    question,
                    st.session_state.messages[:-1], # pass history before this input
                    st.session_state.vector_store
                )
            st.markdown(answer)

            if sources and st.session_state.show_sources:
                with st.expander("📄 Source passages used"):
                    for src in sources:
                        st.markdown(f"**Page {src['page']}**")
                        st.caption(src["snippet"])
                        st.divider()

        st.session_state.messages.append({
            "role":    "assistant",
            "content": answer,
            "sources": sources
        })

if __name__ == "__main__":
    main()