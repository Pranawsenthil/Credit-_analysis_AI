import pdfplumber
from PyPDF2 import PdfReader
import pytesseract
from pdf2image import convert_from_path
import re

def extract_text_from_pdf(filepath):
    """
    Extracts structured text from a PDF, falling back to OCR if the document is scanned.
    Returns a dictionary of sections to prevent generic assumptions.
    """
    raw_text = ""
    # 1. Attempt standard extraction
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    raw_text += extracted + "\n"
    except Exception as e:
        print(f"pdfplumber failed: {e}")
        
    # 2. OCR Fallback if standard extraction yields nothing (scanned PDF)
    if len(raw_text.strip()) < 50:
        try:
            print("Standard extraction failed. Attempting OCR fallback...")
            images = convert_from_path(filepath)
            for img in images:
                raw_text += pytesseract.image_to_string(img) + "\n"
        except Exception as e:
            print(f"OCR failed or not installed properly: {e}\nFalling back to PyPDF2.")
            try:
                reader = PdfReader(filepath)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        raw_text += extracted + "\n"
            except Exception as e2:
                print(f"Ultimate fallback failed: {e2}")

    # 3. Intelligent Section Segmentation
    structured_data = {
        "full_text": raw_text,
        "revenue_section": "",
        "liabilities_section": "",
        "legal_section": "",
        "operational_section": ""
    }
    
    # We use regex to grab chunks of text operating under specific headers
    # These are naive but effective proxies for document structure in prototypes
    
    # Revenue / Profit
    rev_match = re.search(r'(?i)(revenue|income|profit).{0,500}', raw_text, re.DOTALL)
    if rev_match: structured_data["revenue_section"] = rev_match.group(0)
        
    # Debt / Liabilities
    debt_match = re.search(r'(?i)(debt|liabilities|obligations|borrowings).{0,500}', raw_text, re.DOTALL)
    if debt_match: structured_data["liabilities_section"] = debt_match.group(0)
        
    # Legal / Litigation
    legal_match = re.search(r'(?i)(litigation|legal|lawsuit|dispute|fraud|investigation).{0,500}', raw_text, re.DOTALL)
    if legal_match: structured_data["legal_section"] = legal_match.group(0)
        
    # Operations
    ops_match = re.search(r'(?i)(capacity|operations|production|factory).{0,500}', raw_text, re.DOTALL)
    if ops_match: structured_data["operational_section"] = ops_match.group(0)

    return structured_data
