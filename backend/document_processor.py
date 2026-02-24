import fitz  # PyMuPDF
import os

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

def process_file(file_path: str) -> list[dict]:
    """
    Dispatcher to process different file types.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return process_pdf(file_path)
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
