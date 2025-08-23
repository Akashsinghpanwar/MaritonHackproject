# Maritime Virtual Assistant

This is a production-ready, minimal application that demonstrates a powerful RAG (Retrieval-Augmented Generation) pipeline for the maritime industry. It allows users to upload documents like Charter Parties and Statements of Facts, and then ask questions in natural language.

 Maritime Virtual Assistant, a Retrieval-Augmented Generation (RAG) application designed for the maritime industry. This system allows users to upload and query documents like charter parties using natural language, receiving answers with traceable citations. Beyond document interaction, the assistant integrates a backend API offering voyage tools for calculating distances, estimating arrival times, computing laytime, and fetching weather forecasts. The architecture consists of a decoupled frontend and a powerful backend, with a RAG pipeline leveraging LlamaIndex for intelligent document ingestion, indexing, and querying using Large Language Models. The document also provides detailed instructions for local development and cloud deployment using Docker and Render.com, highlighting prerequisites and configuration for various API keys.
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="NotebookLM Mind Map (2).png">
  <img src="NotebookLM Mind Map (2).png" alt="Maritime VA hero" width="1000">
</picture>

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

### A Note from the Developer

I got to know about this project one day before the submission deadline. This is all I could do in one day.
