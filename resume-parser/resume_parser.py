from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

def parse_resume(text: str) -> str:
    """
    Parses a resume text using Langchain and Claude to generate a JSON-resume format.
    """
    llm = ChatAnthropic(model="claude-3-opus-20240229")

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
