import pypdf
from bs4 import BeautifulSoup
import markdown
from pathlib import Path
from google_drive import convert_docx_to_pdf
from fastapi import HTTPException

def extract_text(file_path: Path) -> str:
    """
    Extracts text from a file.
    Supports .pdf, .html, and .md files.
    Converts .docx to .pdf and then extracts text.
    """
    file_extension = file_path.suffix
    text = ""

    if file_extension == ".pdf":
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    elif file_extension == ".html":
        with open(file_path, "r") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            text = soup.get_text()
    elif file_extension == ".md":
        with open(file_path, "r") as f:
            html = markdown.markdown(f.read())
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text()
    elif file_extension == ".docx":
        pdf_path = file_path.with_suffix(".pdf")
        convert_docx_to_pdf(str(file_path), str(pdf_path))
        text = extract_text(pdf_path)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    return text
