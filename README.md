# Zaravya Knowledge Assist

An AI-based company knowledge assistant built using Python, Flask and Google Gemini.

## What it does

- Answers questions about Zaravya and its products
- Uses vector search to find relevant information from the knowledge base
- Uses Gemini to generate answers
- Allows users to upload company documents and ask questions about them
- Provides a simple web interface for asking questions

## Technologies Used

- Python
- Flask
- Google Gemini API
- NumPy
- HTML
- CSS
- JavaScript
- PyPDF

## How it works

The user enters a question in the Zaravya Assistant.

The application converts the question into a vector and compares it with vectors created from the Zaravya knowledge base.

The most relevant information is selected and sent to Gemini to generate the answer.

For the Company Assistant, the user can upload a document and ask questions about that document.

## Project Structure

```text
Zaravya-Knowledge-Assist/
│
├── main.py
├── rag.py
├── index.html
├── style.css
├── script.js
├── company_policy_template.html
├── zaravya.txt
├── requirements.txt
└── .gitignore
