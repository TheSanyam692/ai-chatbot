const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const sidebar = document.getElementById("sidebar");
const historyBox = document.getElementById("chat-history");

input.addEventListener("keypress", e => {
    if (e.key === "Enter") sendMessage();
});

function sendMessage() {
    let text = input.value.trim();
    if (!text) return;

    removeEmpty();
    addMessage(text, "user");

    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: text})
    })
    .then(res => res.json())
    .then(data => addMessage(data.reply, "bot"));

    input.value = "";
}

function addMessage(text, type) {
    let div = document.createElement("div");
    div.className = `message ${type}`;
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeEmpty() {
    let e = document.querySelector(".empty");
    if (e) e.remove();
}

function toggleSidebar() {
    sidebar.classList.toggle("collapsed");
}

function toggleTheme() {
    document.body.classList.toggle("dark");
    document.body.classList.toggle("light");
}

function newChat() {
    fetch("/new_chat", {method: "POST"})
    .then(() => {
        chatBox.innerHTML = `
            <div class="empty">
                <h2>JARVIS AI</h2>
                <p>Futuristic personal assistant</p>
            </div>`;
    });
}
