import fitz  # PyMuPDF
import os
import pandas as pd
import docx
from PIL import Image
from google import genai
from dotenv import load_dotenv

load_dotenv()
try:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))
except Exception as e:
    print(f"Failed to initialize Gemini client for OCR: {e}")
    client = None

def process_pdf(file_path: str) -> list[dict]:
    """
    Reads a PDF using PyMuPDF and returns chunks of text with their page numbers.
    Respects physical layout which is critical for financial tables.
    """
    chunks = []
    try:
        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text").strip()
            if text:
                chunks.append({
                    "text": text,
                    "page": page_num + 1  # 1-indexed for reference
                })
        doc.close()
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return chunks

def process_xlsx(file_path: str) -> list[dict]:
    """
    Reads an Excel file using pandas, converts it to a string representation for ingestion.
    Each sheet is treated as a 'page'.
    """
    chunks = []
    try:
        # Read all sheets into an ordered dictionary
        df_dict = pd.read_excel(file_path, sheet_name=None)
        page_num = 1
        for sheet_name, df in df_dict.items():
            # Convert the dataframe to a string/markdown-like table
            text = f"Sheet Name: {sheet_name}\n\n"
            text += df.to_string(index=False)
            
            if text.strip():
                chunks.append({
                    "text": text,
                    "page": page_num
                })
            page_num += 1
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return chunks

def process_docx(file_path: str) -> list[dict]:
    """
    Reads a docx file and extracts paragraphs.
    """
    chunks = []
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        if text.strip():
            chunks.append({"text": text.strip(), "page": 1})
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return chunks

def process_image(file_path: str) -> list[dict]:
    """
    Uses Gemini API Multimodal OCR to extract text from images and describe charts.
    """
    chunks = []
    if not client:
        print("Gemini client not initialized. Cannot process images.")
        return chunks
        
    try:
        img = Image.open(file_path)
        prompt = "Extract all readable text from this image and provide a brief description of any charts, graphs, or visual data. Return only the extracted text and descriptions."
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=[img, prompt]
        )
        if response.text:
            chunks.append({"text": response.text.strip(), "page": 1})
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return chunks

def process_file(file_path: str) -> list[dict]:
    """
    Dispatcher to process different file types.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return process_pdf(file_path)
    elif ext == ".xlsx":
        return process_xlsx(file_path)
    elif ext == ".docx":
        return process_docx(file_path)
    elif ext in [".png", ".jpg", ".jpeg"]:
        return process_image(file_path)
    elif ext in [".txt", ".csv"]:
        chunks = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    chunks.append({"text": text, "page": 1})
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        return chunks
    return []
