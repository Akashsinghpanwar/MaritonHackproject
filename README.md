
Hi, I’m Samiksha Bagri.
This was my very first hackathon and it has been such a valuable experience. A big thanks to ChatGPT, Anthropic, Google, Jules, and GPT Codex for enabling me to build and learn throughout this project.

By participating in this hackathon, I gained so much knowledge, hands-on experience, and confidence.
Thank you to Maritime for organizing this opportunity—it was truly a great experience!💫

⁹# Maritime Virtual Assistant

This is a production-ready, minimal application that demonstrates a powerful RAG (Retrieval-Augmented Generation) pipeline for the maritime industry. It allows users to upload documents like Charter Parties and Statements of Facts, and then ask questions in natural language.

 Maritime Virtual Assistant, a Retrieval-Augmented Generation (RAG) application designed for the maritime industry. This system allows users to upload and query documents like charter parties using natural language, receiving answers with traceable citations. Beyond document interaction, the assistant integrates a backend API offering voyage tools for calculating distances, estimating arrival times, computing laytime, and fetching weather forecasts. The architecture consists of a decoupled frontend and a powerful backend, with a RAG pipeline leveraging LlamaIndex for intelligent document ingestion, indexing, and querying using Large Language Models. The document also provides detailed instructions for local development and cloud deployment using Docker and Render.com, highlighting prerequisites and configuration for various API keys.
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="NotebookLM Mind Map (2).png">
  <img src="NotebookLM Mind Map (2).png" alt="Maritime VA hero" width="1000">
</picture>
<h1 align="center">Maritime Virtual Assistant ⚓️🤖</h1>
<p align="center">
  AI that understands charter parties, statements of facts, and voyage docs — ask questions and get cited answers.
</p>

<p align="center">
  <a href="https://finalefforts.onrender.com/">
    <img alt="Live Demo" src="https://img.shields.io/badge/Live%20Demo-Open%20App-1b72ff?style=for-the-badge&logo=googlechrome&logoColor=white">
  </a>
  <a href="#">
    <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-🚀-16a34a?style=for-the-badge">
  </a>
  <a href="#">
    <img alt="Python" src="https://img.shields.io/badge/Python-3.12-3670a0?style=for-the-badge&logo=python&logoColor=white">
  </a>
</p>

---

## ✨ What you can do
- 📄 **Upload** a PDF/image/markdown doc (charter party, SOF, etc.)
- 💬 **Ask** natural questions — get concise answers
- 📎 **Citations** back to the source (so you can verify)

## 🚢 Try these right now
1. Click **Live Demo** above.
2. Upload any maritime doc (CP/SOF).
3. Paste a prompt:
   - “When does **laytime start** according to this charter party?” ⏱️  
   - “From this **SOF**, calculate **total laytime counted vs. excluded**.” 📘  
   - “What’s the **demurrage rate** and **despatch** terms?” 💵  
   - “Summarize the **governing law & arbitration** clause.” ⚖️

## 🌟 Why it stands out
- ⚡ **Fast answers** with doc awareness  
- 🧭 Designed for **shipping workflows** (NOR, laytime, demurrage)  
- 🖥️ Clean, responsive UI with a fun vibe ✨

---

<!-- Optional: add a screenshot or short GIF to boost engagement -->
<!-- Replace assets/demo.png with your actual path -->
<p align="center">
  <img src="assets/demo.png" alt="Maritime VA demo" width="800">
</p>

<p align="center">
  If you find this useful, ⭐ the repo — it helps a ton! 🙏
</p>

## Features

-   **Document Q&A:** Chat with your uploaded documents. The assistant can answer questions about contract terms, laytime clauses, demurrage, and more.
-   **Citations:** Every answer is backed by citations from the source documents, ensuring traceability and trust.
-   **Smart Ingestion:** Supports PDF, Markdown, and text files. It uses LlamaParse to intelligently extract content from PDFs, ensuring high-quality data for the RAG pipeline.
-   **Voyage Tools API:** Includes a backend API with tools for calculating voyage distance/ETA, computing laytime, and fetching weather forecasts.
-   **Ready for Deployment:** Comes with a `Dockerfile` and detailed instructions for deploying to cloud services like Render.

## How it Works

The application follows a classic client-server architecture with a decoupled frontend and a powerful backend API.

```
+-----------------+      +------------------------------+
|   Frontend      |      |        Backend (API)         |
| (static HTML,   |----->| (FastAPI, LlamaIndex, Tools) |
|  JS, CSS)       |      +------------------------------+
+-----------------+
```

### Frontend

The frontend is a simple, single-page application built with HTML, CSS, and vanilla JavaScript. It is located in the `static/` directory.

-   It provides a user interface for uploading files and asking questions.
-   It communicates with the backend via asynchronous `fetch` requests to the API endpoints.
-   All user interaction logic is contained within `static/index.html`.

### Backend

The backend is a FastAPI application that exposes several endpoints to serve the application.

-   `GET /`: Serves the main `index.html` frontend.
-   `POST /upload`: Handles file uploads, passes them to the RAG pipeline for ingestion, and stores metadata in Supabase.
-   `POST /chat`: Receives a user's question, queries the RAG pipeline, and returns the answer with citations.
-   `POST /tools/distance`: Calculates voyage distance and ETA.
-   `POST /tools/laytime`: Computes laytime based on provided events.
-   `GET /tools/weather`: Fetches a weather forecast for a given latitude and longitude.

### RAG Pipeline

The core of the application is the RAG pipeline in `sami/app/rag.py`, built using the LlamaIndex framework.

1.  **Ingestion (`add_files`):** When files are uploaded, they are processed. If LlamaParse is enabled, PDFs are sent to the LlamaCloud service to be converted into high-quality Markdown.
2.  **Indexing (`get_index`):** The application uses `SimpleDirectoryReader` to read the processed `.md` and `.txt` files. It then builds a `VectorStoreIndex`, which creates numerical representations (embeddings) of the text chunks. This index is persisted in the `sami/app/storage/vector` directory to avoid costly re-indexing.
3.  **Querying (`query`):** When a user asks a question, the query is converted into an embedding. The system performs a semantic search on the vector index to find the most relevant text chunks from the documents. These chunks, along with the original question, are then passed to a Large Language Model (LLM) like GPT-4o to synthesize a final, human-readable answer.

## Setup and Installation

### Prerequisites

-   Python 3.11+
-   Docker (for containerized deployment)
-   A free [Supabase](https://supabase.com/) account for document metadata storage.
-   API keys for:
    -   [OpenAI](https://platform.openai.com/api-keys)
    -   [LlamaCloud](https://cloud.llamaindex.ai/) (for LlamaParse)
    -   [OpenWeather](https://openweathermap.org/api) (specifically for the **One Call API 3.0**)

### Configuration

The application is configured using environment variables.

1.  Create a file named `.env` in the root directory of the project.
2.  Add the following variables to the file, replacing the placeholder values with your actual credentials:

    ```env
    # OpenAI API Key for embeddings and LLM
    OPENAI_API_KEY="sk-..."

    # LlamaCloud API Key for parsing PDFs
    LLAMA_CLOUD_API_KEY="..."

    # OpenWeather API Key for the weather tool
    # Note: Must be subscribed to the "One Call API 3.0" plan
    WEATHER_API_KEY="..."

    # Supabase credentials for storing document filenames
    SUPABASE_URL="https://<your-project-ref>.supabase.co"
    SUPABASE_KEY="<your-supabase-anon-key>"
    ```

### Local Development

1.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
4.  The application will be available at `http://127.0.0.1:8000`.

## Deployment

This application is ready to be deployed as a Docker container. The following instructions are for Render.com.

### 1. Supabase Table Setup

Before deploying, you need to create a table in your Supabase project to store document metadata.

1.  Go to the "Table Editor" in your Supabase project dashboard.
2.  Create a new table named `documents`.
3.  Define the following columns:
    -   `id` (int8, is identity, primary key)
    -   `created_at` (timestamptz, default: `now()`)
    -   `filename` (text)
4.  Row Level Security (RLS) can be left disabled for simple use cases.

### 2. Deploying to Render

1.  **Push to GitHub:** Ensure your project code, including the `Dockerfile`, is pushed to a GitHub repository.
2.  **Create a New Web Service:** On the Render dashboard, click "New +" and select "Web Service".
3.  **Connect Repository:** Connect your GitHub account and select the project repository.
4.  **Settings:**
    -   **Name:** Give your service a name (e.g., `maritime-assistant`).
    -   **Runtime:** Select `Docker`. Render will automatically detect the `Dockerfile`.
    -   **Region:** Choose a region close to you.
5.  **Environment Variables:** Under the "Environment" section, add all the keys from your `.env` file (`OPENAI_API_KEY`, `LLAMA_CLOUD_API_KEY`, `WEATHER_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`).
6.  **Create Web Service:** Click "Create Web Service". Render will build and deploy your application. Once live, you can access it at the public URL provided by Render.

## Future Possibilities

This application provides a strong foundation that can be extended in many ways:

-   **Tool-Integrated Chat:** The backend could be enhanced to use a "function calling" or "agentic" model. This would allow the LLM to intelligently decide when to use the `distance`, `laytime`, or `weather` tools to answer a question, feeding the tool's output back into its context to provide more accurate, data-driven answers.
-   **Interactive Tool UI:** The frontend could be updated to include forms for using the voyage tools directly, allowing users to perform manual calculations without having to phrase a question for the chat.
-   **Advanced Agentic Behavior:** The RAG pipeline could be converted into a more complex LlamaIndex agent that can perform multi-step reasoning across documents and tools.
-   **Support for More Document Types:** The ingestion pipeline could be expanded to support other common file formats like `.docx`, `.xml`, or `.csv`.

***

### A Note from the samiksha

I got to know about this project one day before the submission deadline. This is all I could do in one day.
> ### A quick note on stack & budget 💙
> I would have loved to use Azure Document Intelligence and Azure Database for this project, but I’m currently constrained to free tiers. To ship a working demo, I used:
>
> - **Supabase** (free tier) for the database  
> - **Render** (free tier) to host the web app live: https://finalefforts.onrender.com/  
> - **RAG with LlamaIndex** and other open-source components
> This app is hosted on Render’s free plan. After periods of inactivity, the service can go into “sleep” mode (cold start).  
> If the webpage doesn’t load at first, give it a little time and refresh — it will wake up and start working automatically.
> This is a **demo**—a proof of what I can build with limited resources. With proper support/budget, I can make this agent **far more intelligent**, scalable, and production-ready (better OCR pipelines, Azure DI integration, stronger retrieval, evals, monitoring, etc.).
>
> What matters is a **chance** and **trust**. Give me that, and I’ll deliver something great. 🚀🙏
> > **Heads-up (Render free tier) 💤**
>

