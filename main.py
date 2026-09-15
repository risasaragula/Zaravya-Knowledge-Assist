from flask import Flask, request, jsonify
from rag import answer_question
import os

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Zaravya Knowledge Assist</title>
        <style>
            body {
                font-family: sans-serif;
                background: #f9f6f0;
                text-align: center;
                padding: 60px;
            }
            .box {
                background: white;
                width: 600px;
                margin: auto;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 3px 10px #ccc;
            }
            .top-buttons {
                text-align: left;
                margin-bottom: 30px;
            }
            .top-buttons button {
                padding: 10px 20px;
                margin-right: 5px;
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
            }
            input {
                width: 70%;
                padding: 12px;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
            .ask-button {
                padding: 12px 20px;
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
            }
            #answer {
                margin-top: 25px;
                text-align: left;
                background: #f4f6f8;
                padding: 15px;
                border-radius: 6px;
                white-space: pre-wrap;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <div class="top-buttons">
                <button onclick="openTemplate()">Template</button>
                <button onclick="document.getElementById('resume').click()">Upload</button>
                <input type="file" id="resume" accept=".pdf,.doc,.docx" style="display: none;" onchange="showResume()">
            </div>
            <h1>Zaravya Knowledge Assist</h1>
            <p>Ask Anything about Zaravya</p>
            <input id="question" placeholder="Type your question...">
            <button class="ask-button" onclick="askQuestion()">ASK</button>
            <div id="answer"></div>
        </div>
        <script>
            async function askQuestion() {
                const question = document.getElementById("question").value.trim();
                const answer = document.getElementById("answer");
                if (!question) {
                    answer.innerText = "Please enter a question.";
                    return;
                }
                answer.innerText = "Thinking...";
                try {
                    const response = await fetch("/ask", {method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            question: question
                        })
                    });
                    const data = await response.json();
                    if (!response.ok) {
                        throw new Error(data.error);
                    }
                    answer.innerText = data.answer;
                } catch (error) {
                    answer.innerText = "Error: " + error.message;
                }
            }
            function openTemplate() {
                alert("Template feature will be added here soon.");
            }
            async function showResume() {
                const file = document.getElementById("resume").files[0];
                if (!file) {
                    return;
                }
                const formData = new FormData();
                formData.append("resume", file);
                try {
                    const response = await fetch("/upload", { method: "POST", body: formData});
                    const data = await response.json();
                    if (!response.ok) {
                        throw new Error(data.error);
                    }
                    alert(data.message + ": " + data.filename);
                } catch (error) {
                    alert("Upload error: " + error.message);
                }
            }
        </script>
    </body>
    </html>
    """

@app.route("/ask", methods=["POST"])
def ask():
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

@app.route("/upload", methods=["POST"])
def upload():
    if "resume" not in request.files:
        return jsonify({
            "error": "No file selected"
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    upload_folder = "uploads"

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)

    file.save(file_path)

    return jsonify({
        "message":
            "Resume uploaded successfully",
        "filename":
            file.filename
    })
if __name__ == "__main__":
    app.run(debug=True)