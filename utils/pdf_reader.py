import pdfplumber


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

    return extracted_text