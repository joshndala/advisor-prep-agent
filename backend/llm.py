import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Initialize the new SDK client
try:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
except Exception as e:
    print(f"Failed to initialize Gemini client: {e}")
    client = None

class SourceDetail(BaseModel):
    document_name: str
    page: int
    extracted_quote: str

class AgendaItem(BaseModel):
    id: str
    topic: str
    insight: str
    action_required: str
    sources: list[SourceDetail]

class PrepBriefSchema(BaseModel):
    client_name: str
    meeting_type: str
    ai_generated_agenda: list[AgendaItem]

def generate_prep_brief(client_id: str, context_chunks: list[dict]) -> dict:
    """
    Calls Gemini API with the context and enforces a strict JSON schema via response_schema.
    """
    if not client:
        return {"error": "Gemini client not initialized. Check API Key."}

    context_str = ""
    for c in context_chunks:
        context_str += f"\n--- Source: {c['document_name']} (Page {c['page']}) ---\n{c['text']}\n"
        
    prompt = f"""
    You are an AI assistant for a financial advisor preparing for a client meeting. 
    Review the following retrieved documents for client '{client_id}'.
    Create a preparatory brief with a list of agenda items.
    Focus on extracting key insights, identifying necessary actions (e.g. 'human_approval_needed'), 
    and tracing exactly where the information came from.
    Include exact quotes in the sources detail. Keep IDs unique.
    
    Retrieved Context:
    {context_str}
    """

    print(f"DEBUG: Generating content with {len(context_chunks)} chunks for {client_id}")

    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=PrepBriefSchema,
                temperature=0.1
            ),
        )
        print("DEBUG: Received response from Gemini")
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generating prep brief: {e}")
        return {"error": str(e)}
