from fastapi import HTTPException
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
import docx
from bs4 import BeautifulSoup
import markdown

def extract_text(file_path: Path) -> str:
    """
    Extracts text from a file.
    Supports .pdf, .docx, .html, and .md files.
    Returns an error for .doc files.
    """
    file_extension = file_path.suffix
    text = ""

    if file_extension == ".doc":
        raise HTTPException(status_code=400, detail="DOC files are not supported. Please convert to DOCX.")
    elif file_extension == ".docx":
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif file_extension == ".pdf":
        loader = PyPDFLoader(str(file_path))
        pages = loader.load_and_split()
        for page in pages:
            text += page.page_content
    elif file_extension == ".html":
        with open(file_path, "r") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            text = soup.get_text()
    elif file_extension == ".md":
        with open(file_path, "r") as f:
            html = markdown.markdown(f.read())
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text()
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    return text
