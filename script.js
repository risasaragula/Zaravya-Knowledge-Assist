// ==========================================
// ZARAVYA ASSIST
// ==========================================

async function askQuestion() {

    const questionInput = document.getElementById("question");
    const answer = document.getElementById("answer");

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    answer.style.display = "block";
    answer.innerText = "Thinking...";

    try {

        const response = await fetch("/ask-zaravya", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        if (!response.ok) {
            answer.innerText = data.error || "Something went wrong.";
            return;
        }

        answer.innerText = data.answer;

    } catch (error) {

        console.error(error);
        answer.innerText = "Something went wrong while getting the answer.";

    }
}


// Enter key for Zaravya Assist
function handleEnter(event) {

    if (event.key === "Enter") {

        event.preventDefault();

        askQuestion();

    }
}



// ==========================================
// COMPANY DOCUMENT ASSIST
// ==========================================

async function askCompany() {

    const questionInput = document.getElementById("company-question");
    const answer = document.getElementById("company-answer");

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    answer.style.display = "block";
    answer.innerText = "Thinking...";

    try {

        const response = await fetch("/ask-company", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        if (!response.ok) {
            answer.innerText = data.error || "Something went wrong.";
            return;
        }

        answer.innerText = data.answer;

    } catch (error) {

        console.error(error);
        answer.innerText = "Something went wrong while getting the answer.";

    }
}


// Enter key for Company Policy
function handleCompanyEnter(event) {

    if (event.key === "Enter") {

        event.preventDefault();

        askCompany();

    }
}



// ==========================================
// FILE UPLOAD
// ==========================================

async function uploadFile() {

    const fileInput = document.getElementById("file");
    const status = document.getElementById("upload-status");

    if (!fileInput.files.length) {
        return;
    }

    const file = fileInput.files[0];

    status.innerText = "Uploading...";

    const formData = new FormData();

    formData.append("file", file);

    try {

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {

            status.innerText =
                data.error || "Upload failed.";

            return;
        }

        status.innerText =
            "✓ " + data.filename + " uploaded successfully.";

    } catch (error) {

        console.error(error);

        status.innerText =
            "Something went wrong while uploading.";

    }
}



// ==========================================
// TEMPLATE POPUP
// ==========================================

function openTemplate() {

    const modal = document.getElementById("template-modal");
    const frame = document.getElementById("template-frame");

    frame.src = "/template";

    modal.style.display = "flex";
}


function closeTemplate() {

    const modal = document.getElementById("template-modal");
    const frame = document.getElementById("template-frame");

    modal.style.display = "none";

    frame.src = "";
}


function downloadTemplate() {

    window.open("/template", "_blank");

}



// ==========================================
// CLOSE TEMPLATE WHEN CLICKING OUTSIDE
// ==========================================

window.addEventListener("click", function(event) {

    const modal = document.getElementById("template-modal");

    if (event.target === modal) {

        closeTemplate();

    }

});

window.addEventListener("keydown", function(event) {

    if (event.key === "Escape") {

        const modal = document.getElementById("template-modal");

        if (modal.style.display === "flex") {

            closeTemplate();

        }
    }

});