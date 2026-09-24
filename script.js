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
            "/ask-company",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: question
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            answer.innerText = data.error;
            return;
        }

        answer.innerText = data.answer;

    } catch (error) {
        answer.innerText = "Something went wrong.";
    }
}