from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_classic.chains.question_answering import load_qa_chain
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import shutil
import tempfile
import uuid

# Load environment variables
load_dotenv()

# Configure OpenAI API for OpenRouter
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY", "")
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

app = FastAPI(title="Cogniva Docs API", description="API for chatting with multiple PDF documents")

# Add CORS middleware to allow React frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=50000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible using ONLY the provided context.

    Formatting rules (STRICT):
    1. Do NOT use bullet points, dashes, or numbering.
    2. Write each point as a separate plain text line.
    3. Leave ONE empty line after each line.
    4. Do NOT combine multiple ideas in one paragraph.
    5. Separate different topics or sections with a blank line.
    6. Do NOT use hyphens connected to words.

    Correct format example:
    Point one

    Point two

    New section point

    Another point

    Incorrect format example:
    - Point one
    - Point two
    Point one and point two together

    If the answer is not available in the provided context, respond exactly with:
    "Answer is not available in the context"

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    
    model = ChatOpenAI(model="openai/gpt-3.5-turbo", temperature=0.3)
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    
    return chain

@app.get("/")
async def root():
    return {"message": "Cogniva Docs API is running!"}

@app.post("/process-pdfs")
async def process_pdfs(files: list[UploadFile] = File(...)):
    """Process uploaded PDF files and create vector store"""
    try:
        # Save uploaded files temporarily
        temp_files = []
        for file in files:
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            shutil.copyfileobj(file.file, temp_file)
            temp_file.close()
            temp_files.append(temp_file.name)
        
        # Process PDFs
        pdf_objects = [open(temp_file, 'rb') for temp_file in temp_files]
        raw_text = get_pdf_text(pdf_objects)
        
        # Close file objects
        for pdf_obj in pdf_objects:
            pdf_obj.close()
        
        # Clean up temporary files
        for temp_file in temp_files:
            os.unlink(temp_file)
        
        # Create text chunks and vector store
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        
        return JSONResponse(content={"message": "PDFs processed successfully"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDFs: {str(e)}")

@app.post("/ask")
async def ask_question(question: str = Form(...)):
    """Ask a question about the processed PDFs"""
    try:
        # Check if FAISS index exists
        if not os.path.exists("faiss_index"):
            raise HTTPException(status_code=400, detail="Please process PDF files first before asking questions.")
        
        # Load embeddings and vector store
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(question)
        
        # Get conversational chain and response
        chain = get_conversational_chain()
        response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
        
        return JSONResponse(content={"answer": response["output_text"]})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)