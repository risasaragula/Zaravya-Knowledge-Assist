async function askQuestion() {
    const question = document.getElementById("question").value.trim();
    const answer = document.getElementById("answer");

    if (!question) {
        answer.innerText = "Please enter a question.";
        return;
    }
    answer.innerText = "Thinking...";
    try {
        const response = await fetch("/ask-zaravya",
            {
                method: "POST",headers: {
                    "Content-Type": "application/json"
                },body: JSON.stringify({
                    question: question
                })
            }
        );
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

async function askCompany() {
    const question = document.getElementById("company-question").value.trim();
    const answer = document.getElementById("company-answer");
    if (!question) {
        answer.innerText = "Please enter a question.";
        return;
    }
    answer.innerText = "Thinking...";
    try {
        const response = await fetch(
            "/ask-company",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },body: JSON.stringify({
                    question: question
                })
            }
        );
        const text = await response.text();
    console.log("Status:", response.status);
    console.log("Response:", text);
    if (!response.ok) {
        throw new Error(text);
    }
    const data = JSON.parse(text);
    answer.innerText = data.answer;
    } catch (error) {
        answer.innerText = "Error: " + error.message;
    }
}

function handleCompanyEnter(event) {
    if (event.key === "Enter") {
        askCompany();
    }
}

function openTemplate() {
    window.open("/template", "_blank");
}

async function uploadFile() {
    const file = document.getElementById("file").files[0];
    if (!file) {
        return;
    }
    const formData = new FormData();
    formData.append("file", file

    );

    try {
        const response = await fetch(
            "/upload",{
                method: "POST", body: formData
            }
        );
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error);
        }
        alert(data.message + ": " + data.filename);
    } catch (error) {
        alert("Upload error: " + error.message);
    }
} 