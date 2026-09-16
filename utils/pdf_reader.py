import io
import pdfplumber
import pytesseract
import fitz
from PIL import Image
import platform


if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = (
        r"D:\workspace\Tesseract-OCR\tesseract.exe"
    )


def extract_text_from_pdf(uploaded_file):
    """
    Ek uploaded PDF file leta hai, har page ka text nikaalta hai,
    aur poora text ek single string ke roop mein return karta hai.
    """
    extracted_text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"

    

    if extracted_text.strip():
        print(f"[DEBUG] Normal extraction se mila: {len(extracted_text)} characters")
        return extracted_text
    
    print("[DEBUG] Normal extraction se kuch nahi mila, OCR try kar rahe hain...")
    
    uploaded_file.seek(0)
    pdf_bytes =uploaded_file.read()
    
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    print(f"[DEBUG] PDF mein total pages: {len(doc)}")
    ocr_text = ""
    
    for page_num,page in enumerate(doc):
        pixmap= page.get_pixmap(dpi=200)
        image=Image.open(io.BytesIO(pixmap.tobytes("png")))
        
        page_text= pytesseract.image_to_string(image)
        print(f"[DEBUG] Page {page_num + 1}: OCR se mila {len(page_text)} characters")
        
        if page_text:
            ocr_text += page_text + "\n"
    print(f"[DEBUG] Total OCR text: {len(ocr_text)} characters")
    return ocr_text
            
        
    