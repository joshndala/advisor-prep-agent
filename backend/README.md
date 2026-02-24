# Advisor Prep Agent - Backend

This directory contains the FastAPI Python backend for the Advisor Prep Agent, responsible for document ingestion, local vector storage, and the retrieval-augmented generation (RAG) pipeline via Google Gemini.

## Core Features

- **Static File Serving**: Mounts the mock data directory utilizing FastAPI `StaticFiles` so the frontend can securely access and render raw source PDF documents.
- **Local Document Ingestion**: Monitors a local data store, seamlessly ingesting PDF, CSV, and TXT files.
- **Physical Layout Parsing**: Utilizes `PyMuPDF` (`fitz`) to extract text logically while respecting document layout constraints and extracting specific page numbers.
- **Vector Database**: Connects to a persistent, local instance of `ChromaDB` for embedding management and vector similarity search.
- **Gemini AI Integration**: Uses the official `google-genai` SDK and the `gemini-2.5-pro` model to generate structured data insights using `BaseModel` JSON schemas.

## Tech Stack
- **Framework**: FastAPI (Uvicorn)
- **Vector DB**: ChromaDB (`chromadb`)
- **LLM API**: Google Gemini (`google-genai`)
- **Document Parsing**: PyMuPDF (`fitz`), Python core libraries
- **Environment**: Python 3.12+ (Virtual Environment `.venv`)

## Setup Instructions

1. **Create Virtual Environment**
   ```bash
   cd backend
   python -m venv venv
   ```

2. **Activate the Virtual Environment**
   ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install fastapi uvicorn pydantic python-dotenv chromadb google-genai pymupdf python-multipart
   ```

4. **Environment Variables**
   Create a `.env` file in the root of the backend folder and provide your Gemini API key.
   ```
   GEMINI_API_KEY=AIzaSy...
   ```

5. **Run the Development Server**
   To test from inside the `/backend` folder:
   ```bash
   # Ensure you use the virtual environment python explicitly if you have global path issues
   ./venv/bin/python -m uvicorn main:app --reload --port 8000
   ```
