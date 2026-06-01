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
        model="gemini-1.5-flash",
        google_api_key=GEMINI_API_KEY
    )

# ── Ingest uploaded PDF ───────────────────────────────────────────────────────
def ingest_pdf(uploaded_file) -> tuple[QdrantVectorStore, int]:
    """Save uploaded file to temp path, chunk it, embed it, store in Qdrant."""
    
    # Write uploaded bytes to a temp file so PyPDFLoader can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Load & split
    loader     = PyPDFLoader(file_path=tmp_path)
    docs       = loader.load()
    splitter   = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    split_docs = splitter.split_documents(docs)
    os.unlink(tmp_path)  # clean up temp file

    # Use filename (without ext) as collection name so each PDF gets its own store
    collection_name = uploaded_file.name.replace(".pdf", "").replace(" ", "_").lower()

    # Embed & store — recreate collection so re-uploads don't duplicate chunks
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

    # Return source pages for citation
    sources = [
        {
            "page":    doc.metadata.get("page", "?") + 1,
            "snippet": doc.page_content[:200] + "..."
        }
        for doc in results
    ]

    return response.content, sources

# ── Streamlit UI ──────────────────────────────────────────────────────────────
def main():
    st.set_page_config(page_title="📚 PDF Study Assistant", page_icon="📚", layout="wide")
    st.title("📚 PDF Study Assistant")
    st.caption("Upload any PDF — textbook, notes, or document — and ask questions about it")

    # ── Sidebar: upload & controls ────────────────────────────────────────────
    with st.sidebar:
        st.header("📂 Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            help="Any size PDF — textbooks, notes, reports"
        )

        if uploaded_file:
            # Only re-ingest if it's a new file
            if st.session_state.get("loaded_file") != uploaded_file.name:
                with st.spinner(f"Reading and indexing **{uploaded_file.name}**... (large files take a moment)"):
                    try:
                        vector_store, chunk_count, collection = ingest_pdf(uploaded_file)
                        st.session_state.vector_store  = vector_store
                        st.session_state.loaded_file   = uploaded_file.name
                        st.session_state.messages      = []
                        st.session_state.collection    = collection
                        st.success(f"✅ Indexed **{chunk_count}** chunks from `{uploaded_file.name}`")
                    except Exception as e:
                        st.error(f"Error ingesting PDF: {e}")
            else:
                st.success(f"✅ `{uploaded_file.name}` already loaded")

        st.markdown("---")

        # Show sources toggle
        st.session_state.show_sources = st.toggle(
            "Show source passages",
            value=st.session_state.get("show_sources", True)
        )

        st.markdown("---")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

        # Info box
        st.markdown("---")
        st.markdown("""
**How it works**
1. Upload any PDF
2. Ask questions in chat
3. AI answers from the document only
4. See exactly which passage was used
        """)

    # ── Main chat area ────────────────────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show placeholder if no PDF loaded
    if "vector_store" not in st.session_state:
        st.info("👈 Upload a PDF from the sidebar to get started")
        return

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            # Show sources for assistant messages if available
            if msg["role"] == "assistant" and msg.get("sources") and st.session_state.show_sources:
                with st.expander("📄 Source passages used"):
                    for src in msg["sources"]:
                        st.markdown(f"**Page {src['page']}**")
                        st.caption(src["snippet"])
                        st.divider()

    # Chat input
    if question := st.chat_input(f"Ask anything about {st.session_state.get('loaded_file', 'your document')}..."):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching document and thinking..."):
                answer, sources = ask(
                    question,
                    st.session_state.messages[:-1],
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
