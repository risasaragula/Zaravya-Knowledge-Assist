import os
from dotenv import load_dotenv
from google import genai
import numpy as np

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
with open("zaravya.txt", "r", encoding="utf-8") as file:
    document = file.read()

def split_document(text):
    words = text.split()
    chunks = []
    for i in range(0, len(words), 300):
        chunk = " ".join(words[i:i + 300])
        chunks.append(chunk)
    return chunks

def create_vector(text):
    response = client.models.embed_content(model="gemini-embedding-001", contents = text)
    return np.array(response.embeddings[0].values)
chunks = split_document(document)
vectors = []
for chunk in chunks:
    vector = create_vector(chunk)
    vectors.append(vector)

def find_similar_text(question):
    question_vector = create_vector(question)
    scores = []
    for vector in vectors:
        score = np.dot(question_vector,vector)
        scores.append(score)
    best_indexes = np.argsort(scores)[-3:]
    results = []
    for index in best_indexes:
        results.append(chunks[index])
    return results
    
def answer_question(question):
    relevant_text = find_similar_text(question)
    context = "\n\n".join(relevant_text)
    prompt = f"""
    Use only the information below to answer the question.
    Do not use your own knowledge.
    Do not say "Based on the document" or "According to the document". 
    Just give the answer directly.
    If the answer is not available, say: "Information not found in the document."
Information:
{context}
Question:
{question}
Answer:
"""
    response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
    return response.text

def answer_from_uploaded_document(question, document_path):
    uploaded_file = client.files.upload(file=document_path)
    prompt = f"""
    Use ONLY the uploaded document to answer the question.
    Do not use your own knowledge.
    Do not say "Based on the document" or "According to the document".
    Just give the answer directly.
    If the answer is not available in the uploaded document, say: "Information not found in the document."
Question:
{question}
Answer:
"""
    response = client.models.generate_content(model="gemini-3.6-flash", contents=[uploaded_file, prompt])
    return response.text