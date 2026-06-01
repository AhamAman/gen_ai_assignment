# 📚 PDF RAG Assistant

A lightweight, local Retrieval-Augmented Generation (RAG) application that allows users to securely upload, index, and chat with PDF documents. Built with Streamlit, LangChain, Qdrant, and Google's Gemini models.

## ⚙️ System Architecture

This application operates on a strict ingestion-to-generation pipeline to prevent LLM hallucinations:

1. **Document Ingestion:** Uploaded PDFs are parsed securely using `PyPDFLoader` and staged in temporary memory.
2. **Chunking & Vectorization:** Text is sliced into 1,000-character chunks with a 200-character overlap to preserve contextual continuity. Chunks are converted into semantic vectors using `GoogleGenerativeAIEmbeddings` (`text-embedding-004`).
3. **Local Vector Storage:** Embeddings are stored in a local **Qdrant** database instance, creating a unique collection for each uploaded document to prevent cross-contamination of contexts.
4. **Contextual Retrieval:** User queries trigger a similarity search ($k=4$), extracting the most mathematically relevant document passages.
5. **Grounded Generation:** The retrieved context is injected into a strict system prompt. **Gemini 1.5 Flash** synthesizes the final answer, explicitly citing the source pages used.

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Orchestration:** LangChain
* **Vector Database:** Qdrant (Local Docker Instance)
* **Embeddings & LLM:** Google Gemini API
* **Data Processing:** PyPDF

