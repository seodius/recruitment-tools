# Resume Parser API

This is a FastAPI application that takes an email address and a resume in `.doc`, `.pdf`, `.html`, or `.md` format, and parses it into a JSON-resume format.

## Features

- Extracts text from various resume formats.
- Converts `.docx` files to `.pdf` using the Google Drive API.
- Parses the resume text into the JSON-resume format using Langchain and Gemini.
- Validates the email address provided in the request against the one found in the resume.
- Stores the original resume, the extracted text, and the parsed JSON.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/resume-parser-api.git
    cd resume-parser-api
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Google Drive API credentials:**
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project.
    - Enable the "Google Drive API".
    - Create credentials for a "Desktop app".
    - Download the `credentials.json` file and place it in the root of the project.

4.  **Configure your Google API Key for Gemini:**
    - Go to the [Google AI Studio](https://aistudio.google.com/).
    - Create a new API key.
    - Set the `GOOGLE_API_KEY` environment variable:
      ```bash
      export GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
      ```
    - Alternatively, you can uncomment and set the `os.environ["GOOGLE_API_KEY"]` line in `resume_parser.py` and `main.py`.

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
- `google_drive.py`: Handles the Google Drive API integration for `.docx` to `.pdf` conversion.
- `text_extractor.py`: Extracts text from different file formats.
- `resume_parser.py`: Parses the resume text using Langchain and Gemini.
- `requirements.txt`: The list of Python dependencies.
- `credentials.json`: Your Google Drive API credentials.
- `resumes/`: The directory where the uploaded resumes, extracted text, and parsed JSON are stored.
