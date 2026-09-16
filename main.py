from flask import Flask, request, jsonify, send_file
from rag import answer_question, answer_from_uploaded_document
import os

app = Flask(__name__)
uploaded_document = ""

@app.route("/")
def home():
    return send_file("index.html")
    
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data["question"].strip()
        if not question:
            return jsonify({
                "error": "Please enter a question"
            }), 400
        if uploaded_document:
            answer = answer_from_uploaded_document(question,uploaded_document)
        else:
            answer = answer_question(question)
        return jsonify({
            "answer": answer
        })
    
    except Exception as e:
        print("Error:", e)
        return jsonify({
            "error": str(e)
        }), 500

@app.route("/upload", methods=["POST"])
def upload():
    global uploaded_document
    if "file" not in request.files:
        return jsonify({
            "error": "No file selected"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    upload_folder = "uploads"

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)

    file.save(file_path)

    uploaded_document = file_path

    print("Uploaded document:")
    print(uploaded_document)

    return jsonify({
        "message": "Uploaded successfully",
        "filename": file.filename
    })
if __name__ == "__main__":
    app.run(debug=True) 