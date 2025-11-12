from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# Set your Google API key
# os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"

def parse_resume(text: str) -> str:
    """
    Parses a resume text using Langchain and Gemini to generate a JSON-resume format.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    prompt = PromptTemplate(
        input_variables=["resume_text"],
        template="""
        Parse the following resume text and return it in the JSON-resume format.
        The JSON should include the following sections: "basics", "work", "education", "skills", "projects", "awards", "publications", "volunteer", "languages", "interests", "references".

        Resume text:
        {resume_text}
        """,
    )

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"resume_text": text})

    return result
