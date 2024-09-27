let isRecording = false;
let mediaRecorder;
let audioChunks = [];
let recordingTimeout;

document.getElementById("send-button").addEventListener("mousedown", (event) => {
    recordingTimeout = setTimeout(() => {
        if (event.button === 0 && document.getElementById("message-input").value === "") {
            isRecording = true;
            document.getElementById("send-button").classList.add("recording");
            navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();
                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };
            });
        }
    }, 3000);
});

document.getElementById("send-button").addEventListener("mouseup", () => {
    clearTimeout(recordingTimeout);
    if (isRecording) {
        isRecording = false;
        document.getElementById("send-button").classList.remove("recording");
        mediaRecorder.stop();
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            audioChunks = [];
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.wav');
            fetch('/upload_audio', {
                method: 'POST',
                body: formData
            }).then(response => response.text()).then(data => {
                addMessage(data, 'bot-message');
            });
        };
    } else {
        sendMessage();
    }
});

document.getElementById("file-input").addEventListener("change", function () {
    const file = this.files[0];
    const formData = new FormData();
    formData.append('file', file);
    document.getElementById("file-label").textContent = file.name; // Mostrar o nome do arquivo anexado
});

document.getElementById("message-input").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    const message = document.getElementById("message-input").value;
    const fileInput = document.getElementById("file-input");
    if (message.trim() !== "") {
        addMessage(message, 'user-message');
        const formData = new FormData();
        formData.append('message', message);
        if (fileInput.files.length > 0) {
            formData.append('file', fileInput.files[0]);
        }
        fetch('/send_message_with_file', {
            method: 'POST',
            body: formData
        }).then(response => response.text()).then(data => {
            addMessage(data, 'bot-message');
        });
        document.getElementById("message-input").value = "";
        document.getElementById("file-label").textContent = "Anexar"; // Resetar o label do arquivo
    }
}

function addMessage(message, className) {
    const messageElement = document.createElement("div");
    messageElement.className = `message ${className}`;
    messageElement.textContent = message;
    document.getElementById("chat-container").appendChild(messageElement);
    document.getElementById("chat-container").scrollTop = document.getElementById("chat-container").scrollHeight;
}

// Alternar entre dark mode e light mode
document.getElementById("theme-toggle").addEventListener("click", function () {
    const bodyClass = document.body.classList;
    if (bodyClass.contains("light-mode")) {
        bodyClass.remove("light-mode");
        bodyClass.add("dark-mode");
        this.textContent = "☀️";
    } else {
        bodyClass.remove("dark-mode");
        bodyClass.add("light-mode");
        this.textContent = "🌙";
    }
});

