import pytest
from fastapi.testclient import TestClient
from main import app
import os
from pathlib import Path

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the resume parser API"}

def test_upload_resume_unsupported_file():
    email = "test@example.com"
    file_content = b"This is a test file."
    files = {"file": ("test.unsupported", file_content, "text/plain")}
    response = client.post("/upload-resume/", data={"email": email}, files=files)
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]

def test_upload_resume_pdf(mocker):
    # Mock the parse_resume function
    mocker.patch(
        "main.parse_resume",
        return_value='{"basics": {"name": "John Doe"}}',
    )

    email = "test@example.com"

    # Create a dummy PDF file
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="This is a test PDF.", ln=1, align="C")
    pdf.cell(200, 10, txt=f"Email: {email}", ln=1, align="C")
    pdf.output("test.pdf")

    with open("test.pdf", "rb") as f:
        files = {"file": ("test.pdf", f, "application/pdf")}
        response = client.post("/upload-resume/", data={"email": email}, files=files)

    assert response.status_code == 200
    assert response.json()["message"] == "Resume parsed successfully."
    assert "basics" in response.json()

    # Clean up created files and directories
    os.remove("test.pdf")
    email_folder_name = email.replace("@", "AT")
    resume_folder = Path("resumes") / email_folder_name
    for f in resume_folder.glob("*"):
        os.remove(f)
    os.rmdir(resume_folder)
