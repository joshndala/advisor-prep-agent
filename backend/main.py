import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import add_document_chunks, get_relevant_chunks, is_document_ingested
from document_processor import process_file
from llm import generate_prep_brief

app = FastAPI(title="Advisor Prep Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MOCK_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mock_data")
os.makedirs(MOCK_DATA_DIR, exist_ok=True)

# Mount the static files route for the frontend to access raw PDFs directly
app.mount("/api/documents", StaticFiles(directory=MOCK_DATA_DIR), name="documents")

router = APIRouter(prefix="/api")

@router.get("/clients")
def get_clients():
    clients = []
    if os.path.exists(MOCK_DATA_DIR):
        for item in os.listdir(MOCK_DATA_DIR):
            if os.path.isdir(os.path.join(MOCK_DATA_DIR, item)):
                clients.append(item)
    return {"clients": clients}

@router.get("/clients/{client_id}/files")
def get_client_files(client_id: str):
    client_dir = os.path.join(MOCK_DATA_DIR, client_id)
    files = []
    if os.path.exists(client_dir):
        for filename in os.listdir(client_dir):
            if os.path.isfile(os.path.join(client_dir, filename)):
                files.append(filename)
    return {"files": files}

def ingest_directory(client_id: str):
    client_dir = os.path.join(MOCK_DATA_DIR, client_id)
    if not os.path.exists(client_dir):
        return
        
    for filename in os.listdir(client_dir):
        file_path = os.path.join(client_dir, filename)
        if os.path.isfile(file_path):
            if not is_document_ingested(client_id, filename):
                chunks = process_file(file_path)
                if chunks:
                    add_document_chunks(client_id, filename, chunks)

@router.post("/upload/{client_id}")
async def upload_file(client_id: str, file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing")
        
    client_dir = os.path.join(MOCK_DATA_DIR, client_id)
    os.makedirs(client_dir, exist_ok=True)
    
    file_path = os.path.join(client_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Ingest document text dynamically
    if not is_document_ingested(client_id, file.filename):
        chunks = process_file(file_path)
        if chunks:
            add_document_chunks(client_id, file.filename, chunks)
            
    return {"filename": file.filename, "status": "Uploaded and ingested successfully"}

@router.post("/generate_prep/{client_id}")
def generate_prep(client_id: str):
    print(f"DEBUG: Endpoint /generate_prep hit for client: {client_id}")
    # Ensure all local directory files are ingested
    ingest_directory(client_id)
    
    query = "financial reports, tax returns, meeting notes, action items, investments, portfolio discussion"
    context_chunks = get_relevant_chunks(client_id, query, n_results=10)
    
    print(f"DEBUG: Retrieved {len(context_chunks)} context chunks from ChromaDB")
    
    if not context_chunks:
        print("DEBUG: No context chunks found, raising 404")
        raise HTTPException(status_code=404, detail="No document context found for this client.")
        
    brief = generate_prep_brief(client_id, context_chunks)
    
    if "error" in brief:
        print(f"DEBUG: Generation error: {brief['error']}")
        raise HTTPException(status_code=500, detail=brief["error"])
        
    print("DEBUG: Successfully generated prep brief")
    return brief

app.include_router(router)
