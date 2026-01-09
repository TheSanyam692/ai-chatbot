const chatBox = document.getElementById("chat-box");
const inputField = document.getElementById("user-input");
const historyList = document.getElementById("history-list");

let chatCount = 1;

// ENTER KEY
inputField.addEventListener("keypress", e => {
    if (e.key === "Enter") sendMessage();
});

// SEND MESSAGE
function sendMessage() {
    let msg = inputField.value.trim();
    if (!msg) return;

    addMessage(msg, "user");
    saveHistory(msg);

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => addMessage(data.reply, "bot"));

    inputField.value = "";
}

// ADD MESSAGE
function addMessage(text, type) {
    let div = document.createElement("div");
    div.className = `message ${type}`;
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// THEME TOGGLE
function toggleTheme() {
    document.body.classList.toggle("dark");
}

// CHAT HISTORY
function saveHistory(msg) {
    let li = document.createElement("li");
    li.innerText = `Chat ${chatCount++}: ${msg.substring(0, 15)}...`;
    historyList.appendChild(li);
}

// NEW CHAT
function newChat() {
    chatBox.innerHTML = "";
}
