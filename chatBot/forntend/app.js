const chat = document.getElementById("chat");
const input = document.getElementById("message");

/* ==========================
   🔊 TEXTO A VOZ (BOT)
========================== */
function speak(text) {
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "es-ES";
    window.speechSynthesis.speak(speech);
}

/* ==========================
   📤 ENVIAR MENSAJE
========================== */
function sendMessage() {
    const msg = input.value.trim();
    if (!msg) return;

    addMessage(msg, "user");
    input.value = "";

    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => {
        addMessage(data.response, "bot");
        speak(data.response);
    })
    .catch(() => {
        addMessage("Error al conectar con el servidor", "bot");
    });
}

/* ==========================
   💬 MOSTRAR MENSAJES
========================== */
function addMessage(text, type) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", type);
    msgDiv.textContent = text;
    chat.appendChild(msgDiv);
    chat.scrollTop = chat.scrollHeight;
}

/* ==========================
   🎤 VOZ A TEXTO
========================== */
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.lang = "es-ES";
recognition.interimResults = false;
recognition.continuous = false;

function startVoice() {
    recognition.start();
}

recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    input.value = text;
    sendMessage();
};

recognition.onerror = (event) => {
    alert("Error de voz: " + event.error);
};
