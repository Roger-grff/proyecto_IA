document.addEventListener("DOMContentLoaded", () => {

    /* ========================
       RESET AL RECARGAR
    ========================== */
    localStorage.removeItem("userName");

    /* ==========================
       FLAGS
    ========================== */
    let userInteracted = false; 
    let greetedWithAudio = false; 

    /* ==========================
       ELEMENTOS DOM
    ========================== */
    const chat = document.getElementById("chat");
    const input = document.getElementById("message");
    const toggleVoiceBtn = document.getElementById("toggleVoice");

    /* ==========================
       ESTADO DE VOZ
    ========================== */
    let voiceEnabled = localStorage.getItem("voiceEnabled");
    if (voiceEnabled === null) voiceEnabled = true;
    else voiceEnabled = voiceEnabled === "true";

    toggleVoiceBtn.textContent = voiceEnabled ? "🔊 Voz: ON" : "🔇 Voz: OFF";

    toggleVoiceBtn.addEventListener("click", () => {
        voiceEnabled = !voiceEnabled;
        localStorage.setItem("voiceEnabled", voiceEnabled);

        if (!voiceEnabled) window.speechSynthesis.cancel();

        toggleVoiceBtn.textContent = voiceEnabled ? "🔊 Voz: ON" : "🔇 Voz: OFF";
    });

    /* ==========================
       DETECTAR PRIMERA INTERACCIÓN
    ========================== */
    function handleUserInteraction() {
        userInteracted = true;
        if (!greetedWithAudio) {
            speak(`Hola ${userName}, soy tu asistente de programación.
         Escribe tu primera pregunta cuando quieras.`);
            greetedWithAudio = true;
        }
    }

    document.addEventListener("click", handleUserInteraction, { once: true });
    document.addEventListener("keydown", handleUserInteraction, { once: true });

    /* ==========================
       NOMBRE DEL USUARIO
    ========================== */
    let userName = localStorage.getItem("userName");
    if (!userName) {
        userName = prompt("👋 Hola, ¿cómo te llamas?");
        if (!userName || userName.trim() === "") userName = "Estudiante";
        localStorage.setItem("userName", userName);
    }

    /* ==========================
       SALUDO INICIAL (SOLO TEXTO)
    ========================== */
    addBotMessage(
        `Hola ${userName} 👋, soy tu asistente de programación.
         Escribe tu primera pregunta cuando quieras.`,
        1
    );

    /* ==========================
       TEXTO A VOZ
    ========================== */
    function speak(text) {
        if (!voiceEnabled || !userInteracted) return;

        window.speechSynthesis.cancel();
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = "es-ES";
        window.speechSynthesis.speak(speech);
    }

    /* ==========================
       ENVIAR MENSAJE
    ========================== */
    function sendMessage() {
        const msg = input.value.trim();
        if (!msg) return;

        addUserMessage(msg);
        input.value = "";

        fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg })
        })
        .then(res => res.json())
        .then(data => {
            addBotMessage(data.response, data.confidence);
            speak(data.response);
        })
        .catch(() => {
            addBotMessage("❌ Error al conectar con el servidor", 0);
        });
    }

    /* ==========================
       ENTER PARA ENVIAR
    ========================== */
    input.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            handleUserInteraction(); 
            sendMessage();
        }
    });

    /* ==========================
       MENSAJE USUARIO
    ========================== */
    function addUserMessage(text) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", "user");
        msgDiv.innerHTML = `<b>${userName}:</b> ${text}`;
        chat.appendChild(msgDiv);
        chat.scrollTop = chat.scrollHeight;
    }

    /* ==========================
       MENSAJE BOT
    ========================== */
    function addBotMessage(text, confidence) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", "bot");

        let level = "low";
        if (confidence >= 0.7) level = "high";
        else if (confidence >= 0.4) level = "medium";

        msgDiv.innerHTML = `
            <div>${text}</div>
            <div class="confidence ${level}">
                Confianza del modelo: ${confidence}
            </div>
        `;

        chat.appendChild(msgDiv);
        chat.scrollTop = chat.scrollHeight;
    }

    /* ==========================
       VOZ A TEXTO
    ========================== */
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.lang = "es-ES";
    recognition.interimResults = false;
    recognition.continuous = false;

    window.startVoice = function () {
        handleUserInteraction(); 
        recognition.start();
    };

    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        input.value = text;
        sendMessage();
    };

    recognition.onerror = (event) => {
        alert("Error de voz: " + event.error);
    };

});
