# Maritime Virtual Assistant (RAG + Azure Document Intelligence)

This is a production-ready minimal app that:
- Parses PDFs/images with **Azure Document Intelligence** (OCR + tables → Markdown + JSON).
- Builds a **RAG** index with **LlamaIndex** (OpenAI or local embeddings).
- Lets you **chat** with your documents and get **citations**.
- Provides tools for **Distance/ETA** and a **basic Laytime calculator**.
- Ships with **sample CP + SOF** to test immediately.

## 1) Setup

### Python
- Recommended: Python 3.11 (Windows PowerShell)
- Create venv and install packages:
```powershell
python -m venv venv
venv\Scripts\activate
pip install -U -r requirements.txt
