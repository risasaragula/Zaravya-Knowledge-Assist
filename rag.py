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
    Do not say "Based on the document" or
    "According to the document".
    Just give the answer directly.
    If the answer is not available in the document, say:
    "Information not found in the document."

    Zaravya Knowledge Document:
    {document}
    Question:
    {question}
    Answer:
    """
    response = client.models.generate_content(
        model="gemini-3.6-flash", contents=prompt
        )
    return response.text

def answer_from_uploaded_document(question, document_path):
    uploaded_file = client.files.upload(file=document_path)

    prompt = f"""
    Use ONLY the uploaded document to answer the question.
    Do not use information from your own knowledge.
    Do not say "Based on the document" or
    "According to the document".
    Just give the answer directly.
    If the answer is not available in the uploaded document, say:
    "Information not found in the document."

    Question:
    {question}
    Answer:
    """
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[uploaded_file,prompt]
    )
    return response.text