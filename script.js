async function askQuestion() {
    const question = document.getElementById("question").value.trim();
    const answer = document.getElementById("answer");
    if (!question) {
        answer.innerText = "Please enter a question.";
        return;
    }
    answer.innerText = "Thinking...";
    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }, body: JSON.stringify({
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
function handleEnter(event) {
    if (event.key === "Enter") {
        askQuestion();
    }
}
function openTemplate() {
    alert("Template feature will be added here soon.");
}
async function uploadFile() {
    const file = document.getElementById("file").files[0];
    if (!file) {
        return;
    }
    const formData = new FormData();
    formData.append("file", file);
    try {
        const response = await fetch("/upload", {
            method: "POST", body: formData
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error);
        }
        alert(data.message + ": " + data.filename);
    } catch (error) {
        alert("Upload error: " + error.message);
    }
}