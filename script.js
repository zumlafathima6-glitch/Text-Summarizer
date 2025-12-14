const inputText = document.getElementById("inputText");
const charCount = document.getElementById("charCount");
const summarizeBtn = document.getElementById("summarizeBtn");
const summaryOutput = document.getElementById("summaryOutput");
const loader = document.querySelector(".loader");
const btnText = document.querySelector(".btn-text");

inputText.addEventListener("input", () => {
    charCount.innerText = `${inputText.value.length} characters`;
});

summarizeBtn.addEventListener("click", () => {
    const text = inputText.value.trim();

    if (!text) {
        alert("Please enter some text!");
        return;
    }

    loader.style.display = "block";
    btnText.style.visibility = "hidden";

    fetch("http://127.0.0.1:5000/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    })
    .then(res => res.json())
    .then(data => {
        summaryOutput.innerText = data.summary;
    })
    .catch(() => {
        summaryOutput.innerText = "❌ Error connecting to server.";
    })
    .finally(() => {
        loader.style.display = "none";
        btnText.style.visibility = "visible";
    });
});
