# 📚 PDF Study Assistant (RAG App)

A lightweight, local Retrieval-Augmented Generation (RAG) study assistant that allows you to upload, index, and ask questions about PDF documents. 

By default, the application is pre-loaded with **nodejs.pdf** so you can run it and start asking questions instantly without waiting for any ingestion!

---

## ⚙️ Architecture & Key Design Decisions

During development, several key design choices were made to optimize speed, reliability, and cost-efficiency:

### 1. Local On-Disk Qdrant Storage (No Docker Required)
* **Decision:** We configured Qdrant to run in **local on-disk mode** (`qdrant_storage/` directory) instead of spinning up a Docker container.
* **Benefits:** 
  * Zero setup overhead (no Docker Desktop or daemon required).
  * Extremely lightweight database footprint.
  * Direct filesystem verification (you can see the database files created directly in the project workspace).

### 2. Local Offline Embeddings (FastEmbed)
* **Decision:** We migrated from Google's Cloud Embedding API (`gemini-embedding-001`) to Qdrant's native **FastEmbed** (`BAAI/bge-small-en-v1.5` 384-dimension) library.
* **Benefits:**
  * **Zero Rate Limits:** Completely bypasses the Gemini Free Tier daily limits (1,000 requests/day), ensuring the app never crashes from API exhausts.
  * **Extreme Speed:** Embeds the entire 266-chunk Node.js study guide in under 3 seconds on a standard local CPU (compared to minutes of sequential cloud calls).
  * **Privacy & Cost:** Documents are vectorized completely offline on your own machine.

### 3. Default Document Auto-Loading
* **Decision:** The application automatically scans the local Qdrant collection on startup.
* **Benefits:** If `nodejs.pdf` has already been pre-indexed (which we did during setup), the app loads the vector index **instantly (<1ms)** at startup. You do not have to upload the file to start querying it.

### 4. Grounded Generation Citations (Gemini 2.5 Flash)
* **Decision:** We pair the retrieved context with a strict system prompt and feed it to **Gemini 2.5 Flash** for final synthesis.
* **Benefits:** The AI only answers using the provided context and provides clickable/expandable page citations, pointing you directly to the exact page in the PDF where the answer was found.

---

## 🚨 Troubleshooting & Development Errors Solved

Here are the specific errors encountered during development and how they were resolved:

### 1. Gemini Embedding Quota Exhaustion (`429 RESOURCE_EXHAUSTED`)
* **The Error:** Initially, attempting to embed the 266 text chunks using Gemini's API (`models/gemini-embedding-001`) triggered concurrency errors. Even when throttled sequentially (with `time.sleep(0.7)`), we eventually hit the strict **1,000 daily embedding requests limit** on the Gemini Free Tier API key, resulting in:
  `Quota exceeded for metric: generativelanguage.googleapis.com/embed_content_free_tier_requests`
* **The Solution:** We replaced Google Generative AI Embeddings with the local `FastEmbedEmbeddings` model. This shifted the document vectorization entirely offline onto your local CPU, bypassing the Gemini API limits completely.

### 2. Vector Shape Mismatch Error
* **The Error:** After switching embedding models, running ingestion triggered the following error:
  `ValueError: could not broadcast input array from shape (384,) into shape (3072,)`
  This happened because the database collection on disk was originally built using Gemini's 3,072-dimension embeddings, which conflicted with FastEmbed's 384-dimension output.
* **The Solution:** We cleanly wiped the `qdrant_storage/` folder on disk and recreated the database collection with `size=384` to match FastEmbed's parameters.

### 3. Qdrant File Locking Conflict
* **The Error:** Force-terminating background tasks that were writing to the local Qdrant database left lock files behind, causing the client to hang or throw warnings during subsequent executions:
  `ModuleNotFoundError: import of msvcrt halted; None in sys.modules` (associated with the `portalocker` library used by Qdrant to manage file access).
* **The Solution:** We terminated all overlapping background processes and ran clean, unbuffered runs (`python -u`) after wiping the locks/storage folder, ensuring a single clean process created the database.

---

## 📂 Project Structure

* **`rag_1.py`**: The main Streamlit web application. Contains the UI, auto-loading logic, similarity retrieval, and LLM orchestration.
* **`nodejs.pdf`**: The default Node.js study guide provided in the project.
* **`qdrant_storage/`**: The local directory containing the vectorized Qdrant collection files (automatically ignored by Git).
* **`requirements.txt`**: The complete list of required libraries.

---

## 🛠️ Setup & Installation

### 1. Configure Secrets
Ensure you have a `.env` file inside the `Assignment 3/` folder (or project root) with your Gemini API key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 2. Virtual Environment Setup
Ensure your local Python virtual environment is active and up to date:
```powershell
# Navigate to the folder
cd "E:\Data cohort\gen_ai_assignment\Assignment 3"

# Activate your environment
..\.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

---

## 🚀 Usage

### Running the App
Start the Streamlit application:
```powershell
streamlit run rag_1.py
```

