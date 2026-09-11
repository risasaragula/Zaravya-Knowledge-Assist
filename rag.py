import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

with open("zaravya.txt", "r", encoding="utf-8") as file:
    document = file.read()


def answer_question(question):

    prompt = f"""
Use the following Zaravya knowledge document to answer the question.

Answer only using the information given in the document.

If the answer is not available in the document, say:
"Information not found in the document."

Zaravya Knowledge Document:
{document}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text