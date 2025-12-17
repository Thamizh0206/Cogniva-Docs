# Cogniva Docs - FastAPI Backend

This is the FastAPI backend for Cogniva Docs. It provides API endpoints for processing PDF files and answering questions about their content.

## Setup Instructions

1. **Make sure you're in the main project directory:**
   ```bash
   cd Multi-PDFs_ChatApp_AI-Agent
   ```

2. **Activate the virtual environment:**
   ```bash
   .\multpdf_env\Scripts\Activate.ps1
   ```

3. **Install dependencies (if not already installed):**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the FastAPI server:**
   ```bash
   python api.py
   ```

   The API will be available at http://localhost:8000

## API Endpoints

- `GET /` - Health check endpoint
- `POST /process-pdfs` - Process uploaded PDF files
- `POST /ask` - Ask a question about the processed PDFs

## Environment Variables

Make sure your `.env` file contains your OpenRouter API key:
```
OPENROUTER_API_KEY=your-openrouter-api-key-here
```

## How It Works

1. **PDF Processing:**
   - Upload PDF files through the `/process-pdfs` endpoint
   - Extract text from PDFs using PyPDF2
   - Split text into chunks using RecursiveCharacterTextSplitter
   - Create embeddings using OpenAI's text-embedding-ada-002 model via OpenRouter
   - Store embeddings in a FAISS vector database

2. **Question Answering:**
   - Receive questions through the `/ask` endpoint
   - Search for relevant text chunks in the FAISS database
   - Use OpenAI's GPT-3.5-turbo model via OpenRouter to generate answers
   - Return detailed answers based on the PDF content

## Development

To modify the backend:

1. Edit `api.py` for the main API logic
2. The PDF processing and question answering functions are defined in this file
3. The FAISS vector database is saved in the `faiss_index` directory

## Models Used

- **Embeddings Model:** text-embedding-ada-002 (via OpenRouter)
- **Chat Model:** openai/gpt-3.5-turbo (via OpenRouter)

## CORS Configuration

The backend is configured to allow CORS from any origin for development purposes. In production, you should restrict this to your frontend's domain.