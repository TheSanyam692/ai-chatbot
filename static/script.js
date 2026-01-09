const inputField = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

// Send message on Enter key
inputField.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    let message = inputField.value.trim();
    if (message === "") return;

    // User message
    let userDiv = document.createElement("div");
    userDiv.className = "message user";
    userDiv.innerText = message;
    chatBox.appendChild(userDiv);

    inputField.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        let botDiv = document.createElement("div");
        botDiv.className = "message bot";
        botDiv.innerText = data.reply;
        chatBox.appendChild(botDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}
