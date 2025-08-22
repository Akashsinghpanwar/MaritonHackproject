# Maritime Virtual Assistant (RAG + Azure Document Intelligence)

This is a production-ready minimal app that:
- Parses PDFs/images with **LlamaParse** (from LlamaCloud).
- Builds a **RAG** index with **LlamaIndex** (OpenAI or local embeddings).
- Lets you **chat** with your documents and get **citations**.
- Provides tools for **Distance/ETA**, **Laytime**, and **Weather**.
- Ships with **sample CP + SOF** to test immediately.

## 1) Local Development Setup

### API Keys & Supabase
This application requires API keys and Supabase credentials.
1.  **Supabase:** Create a new project on [Supabase](https://supabase.com/). In your project settings, find your API URL and `anon` key.
2.  **API Keys:** You will also need API keys for OpenAI, LlamaParse, and OpenWeather.
3.  **Environment File:** Copy the `.env.example` file to `.env` and fill in all the required keys and the Supabase URL.

### Python
- Recommended: Python 3.11
- Create a virtual environment and install packages:
  ```bash
  python -m venv venv
  source venv/bin/activate
  pip install -U -r requirements.txt
  ```
- Run the application:
  ```bash
  uvicorn main:app --reload
  ```
- The application will be available at `http://127.0.0.1:8000`.

## 2) Deployment on Render.com

This application is ready to be deployed as a Docker container on Render.com.

### Supabase Table
Before deploying, you need to create a table in your Supabase database. Go to the "Table Editor" in your Supabase project and create a new table named `documents` with the following columns:
- `id` (int8, is identity, primary key)
- `created_at` (timestamptz, default now())
- `filename` (text)
Make sure to enable RLS (Row Level Security) for the table if you want to control access. For a simple setup, you can leave it disabled.

### Deploying to Render
1.  **Push to GitHub:** Make sure your code is pushed to a GitHub repository.
2.  **Create a New Web Service:** On the Render dashboard, click "New +" and select "Web Service".
3.  **Connect Repository:** Connect your GitHub account and select the repository for this project.
4.  **Settings:**
    -   **Name:** Give your service a name (e.g., `maritime-assistant`).
    -   **Runtime:** Select `Docker`. Render will automatically detect the `Dockerfile`.
    -   **Region:** Choose a region close to you.
    -   **Branch:** Select the branch you want to deploy (e.g., `main`).
5.  **Environment Variables:** Under "Advanced", go to the "Environment" section. Add all the keys from your `.env` file as environment variables (`OPENAI_API_KEY`, `LLAMA_CLOUD_API_KEY`, `OPENWEATHER_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`).
6.  **Create Web Service:** Click "Create Web Service". Render will start building and deploying your application. Once it's live, you can access it at the URL provided by Render.
