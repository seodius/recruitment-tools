from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv

load_dotenv()
import datetime
import re
from pathlib import Path
from text_extractor import extract_text
from resume_parser import parse_resume
import json

app = FastAPI()

class ResumeUpload(BaseModel):
    email: EmailStr

@app.get("/")
def read_root():
    return {"message": "Welcome to the resume parser API"}

@app.post("/upload-resume/")
async def upload_resume(email: EmailStr = Form(...), file: UploadFile = File(...)):
    # Create a folder for the email address (change "@" into "AT") if not exists.
    email_folder_name = email.replace("@", "AT")
    resume_folder = Path("resumes") / email_folder_name
    resume_folder.mkdir(parents=True, exist_ok=True)

    # Store the original as upload-[datetime now].[extention]
    now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_extension = Path(file.filename).suffix
    original_filepath = resume_folder / f"upload-{now}{file_extension}"

    with open(original_filepath, "wb") as buffer:
        buffer.write(await file.read())

    # Extract the txt from the uploaded document.
    try:
        extracted_text = extract_text(original_filepath)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {e}")

    # Store the text as upload-[datetime].txt
    text_filepath = resume_folder / f"upload-{now}.txt"
    with open(text_filepath, "w") as f:
        f.write(extracted_text)

    # Parse the main email address from the uploaded document.
    parsed_email = re.search(r'[\w\.-]+@[\w\.-]+', extracted_text)

    # Compare parsed email with email provided in the endpoint.
    if not parsed_email or parsed_email.group(0) != email:
        raise HTTPException(status_code=400, detail="Email address in resume does not match the provided email.")

    # Parse the txt using langchain and gemini into JSON-resume format.
    try:
        parsed_resume_json = parse_resume(extracted_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {e}")

    # Store the json as parsed-[datetime now].json
    json_filepath = resume_folder / f"parsed-{now}.json"
    with open(json_filepath, "w") as f:
        f.write(parsed_resume_json)

    try:
        # Load the JSON string into a Python dictionary
        resume_data = json.loads(parsed_resume_json)
        # Extract the "basics" section
        basics_section = resume_data.get("basics", {})
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding parsed JSON.")

    return {"message": "Resume parsed successfully.", "basics": basics_section}
