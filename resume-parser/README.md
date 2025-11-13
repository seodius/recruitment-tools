# Resume Parser API

This is a FastAPI application that takes an email address and a resume in `.doc`, `.pdf`, `.html`, or `.md` format, and parses it into a JSON-resume format.

## Features

- Extracts text from various resume formats.
- Extracts text from `.docx` files using `python-docx`.
- Extracts text from `.pdf` files using `PDFLoader` from `langchain`.
- Parses the resume text into the JSON-resume format using Langchain and Gemini.
- Validates the email address provided in the request against the one found in the resume.
- Stores the original resume, the extracted text, and the parsed JSON.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/resume-parser-api.git
    cd resume-parser-api/resume-parser
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your Google API Key for Gemini:**
    - Create a `.env` file by copying the `.env.example` file:
      ```bash
      cp .env.example .env
      ```
    - Go to the [Google AI Studio](https://aistudio.google.com/).
    - Create a new API key.
    - Open the `.env` file and add your Google API key:
      ```
      GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
      ```

## Usage

1.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```

2.  **Access the API documentation:**
    Open your browser and go to `http://127.0.0.1:8000/docs` to see the Swagger UI documentation.

3.  **Upload a resume:**
    Use the `/upload-resume/` endpoint to upload a resume. You'll need to provide your email address and the resume file.

## Project Structure

- `main.py`: The main FastAPI application.
- `text_extractor.py`: Extracts text from different file formats.
- `resume_parser.py`: Parses the resume text using Langchain and Gemini.
- `requirements.txt`: The list of Python dependencies.
- `resumes/`: The directory where the uploaded resumes, extracted text, and parsed JSON are stored.
