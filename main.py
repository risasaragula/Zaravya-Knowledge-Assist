from flask import Flask, request, jsonify, send_file
from rag import answer_question, answer_from_uploaded_document
import os
import webbrowser

app = Flask(__name__)
uploaded_document = ""

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/template")
def template():
    return send_file("company_policy_template.html")

@app.route("/style.css")
def style():
    return send_file("style.css")

@app.route("/script.js")
def script():
    return send_file("script.js")

@app.route("/ask-zaravya", methods=["POST"])
def ask_zaravya():
    try:
        data = request.get_json()
        question = data["question"].strip()
        if not question:
            return jsonify({
                "error": "Please enter a question"
            }), 400
        answer = answer_question(question)
        return jsonify({
            "answer": answer
        })
    except Exception as e:
        print("Error:", e)
        return jsonify({
            "error": str(e)
        }), 500

@app.route("/ask-company", methods=["POST"])
def ask_company():
    try:
        data = request.get_json()
        question = data["question"].strip()
        if not question:
            return jsonify({
                "error": "Please enter a question"
            }), 400
        if not uploaded_document:
            return jsonify({
                "error": "Please upload a document first."
            }), 400
        answer = answer_from_uploaded_document(question, uploaded_document)
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

    file_path = os.path.join(
        upload_folder,
        file.filename
    )

    file.save(file_path)

    uploaded_document = file_path

    print("Uploaded document:")
    print(uploaded_document)

    return jsonify({
        "message": "Uploaded successfully", "filename": file.filename
    })

if __name__ == "__main__":
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get("chrome").open("http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)