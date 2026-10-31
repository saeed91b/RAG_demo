# RAG Demo

RAG Demo is a question-answering app for PDF documents. Upload a PDF through the
Streamlit chat interface, then ask questions about its contents. The FastAPI
backend extracts and splits the document, creates embeddings, retrieves relevant
text, and sends the context to a Gemini model to generate an answer.

## Technology stack

- Python
- Streamlit client
- FastAPI API
- LangChain for document loading, text splitting, retrieval, and Gemini integration
- Google Gemini `gemini-embedding-2-preview` for embeddings
- Google Gemini `gemini-3.5-flash-lite` for answer generation
- In-memory vector store for document retrieval

## Run locally

1. Clone the repository and navigate to the project root:

   ```powershell
   git clone https://github.com/saeed91b/RAG_demo
   cd RAG_demo
   ```
2. Create and activate the Conda environment from the included dependency file:

   ```powershell
   conda create --name rag-demo --file requirements.txt
   conda activate rag-demo
   ```

3. Rename `.env.example` to `.env` and replace the placeholder value for `GOOGLE_API_KEY` in `.env` with your key.


4. Start the API from the `backend` directory:

   ```powershell
   cd backend
   uvicorn api:app 
   ```

5. In a separate terminal, from the project root and with the Conda environment
   activated, start the Streamlit client:

   ```powershell
   streamlit run client.py
   ```

Open the local Streamlit URL shown in the terminal, upload a PDF smaller than
10 MB, and ask questions about it. The API listens on `http://localhost:8000`.

## Run with Docker

Create a `.env` file from `.env.example` and set your `GOOGLE_API_KEY`, then build and run the app from the project root:

```powershell
docker build -t rag-demo .
docker run --rm --env-file .env -p 8501:8501 -p 8000:8000 rag-demo
```

Open `http://localhost:8501` to use the app.
