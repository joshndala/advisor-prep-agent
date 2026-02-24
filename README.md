# Advisor Prep Agent

Advisor Prep Agent is a local-first, AI-native web application designed to solve a legacy workflow in wealth management: synthesizing messy, unstructured client documents into an actionable, verifiable prep brief for financial advisors.

This project demonstrates a clear "human-in-the-loop" decision boundary through a robust verification UI, allowing advisors to approve or discard AI-generated insights before exporting a finalized agenda.

### LINK TO DEMO: https://www.youtube.com/watch?v=GLi2iVKhAho

## Architecture

The project is structured as a monorepo containing two main parts:
- **`frontend/`**: A Vue 3 + Vite application featuring a modern split-screen interface.
- **`backend/`**: A FastAPI Python server utilizing a multimodal Retrieval-Augmented Generation (RAG) pipeline with ChromaDB and Google Gemini.

## Data Flow & RAG Pipeline

1. **Ingestion**: The backend monitors a simulated internal data lake (`mock_data/{client_id}/`). Documents (PDF, TXT, CSV) placed here or uploaded via the UI are automatically parsed using `PyMuPDF`, chunked, and vectorized into a local **ChromaDB**.
2. **Generation**: When a prep brief is requested, the backend queries ChromaDB for relevant context chunks and passes them to the **Gemini 2.5 Pro** model. The model is forced to return strict, parsable JSON using the `google-genai` SDK's structured outputs (`response_schema`).
3. **Traceability**: Every AI-generated insight is strictly tied to a source document and page number, enabling full Explainable RAG.
4. **Human-in-the-Loop**: The frontend displays the generated agenda. Advisors trace insights back to the source document using the integrated PDF Viewer and explicitly "Approve" or "Discard" each item.
5. **Finalization**: Only approved items can be exported and copied to the clipboard for use in a CRM or final meeting brief.

## Setup & Execution

### Prerequisites
- Node.js (v18+)
- Python (3.12+)
- A [Google Gemini API Key](https://aistudio.google.com/)

### Running the Application

1. **Start the Backend server:** Follow instructions in `backend/README.md`.
2. **Start the Frontend client:** Follow instructions in `frontend/README.md`.

Once both are running, open your browser to the local Vite URL (usually `http://localhost:5173`) to use the application.
