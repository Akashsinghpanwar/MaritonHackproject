# Maritime Virtual Assistant (RAG + Azure Document Intelligence)

This is a production-ready minimal app that:
- Parses PDFs/images with **LlamaParse** (from LlamaCloud).
- Builds a **RAG** index with **LlamaIndex** (OpenAI or local embeddings).
- Lets you **chat** with your documents and get **citations**.
- Provides tools for **Distance/ETA**, **Laytime**, and **Weather**.
- Ships with **sample CP + SOF** to test immediately.

## 1) Setup

### API Keys
This application requires API keys for OpenAI, LlamaParse, and OpenWeather.
1.  Copy the `.env.example` file to `.env`.
2.  Fill in the required API keys in the `.env` file.

### Python
- Recommended: Python 3.11 (Windows PowerShell)
- Create venv and install packages:
```powershell
python -m venv venv
venv\Scripts\activate
pip install -U -r requirements.txt
