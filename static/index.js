document.addEventListener("DOMContentLoaded", () => {
    // Get DOM elements
    const recordBtn = document.getElementById("record-btn");
    const playBtn = document.getElementById("play-btn");
    const transcriptEl = document.getElementById("transcript");
    const translationEl = document.getElementById("translation");
    const inputLang = document.getElementById("input_language");
    const outputLang = document.getElementById("output_language");
    const modelSelect = document.getElementById("model");

    // Initialize variables
    let recognition;
    let isRecording = false;
    let savedTranslation = "";
    let lastTranscript = "";

    // Function to send text to the REST API
    async function sendTextToAPI(text) {
        const model = modelSelect.value;
        const apiUrl = `/translate/${model}/`; // Adjust to match FastAPI routes

        try {
            const response = await fetch(apiUrl, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    text: text,
                    input_lang: inputLang.value,
                    output_lang: outputLang.value
                })
            });

            if (!response.ok) {
                throw new Error(`API error: ${response.statusText}`);
            }

            const data = await response.json();
            if (data.translated_text) {
                savedTranslation = data.translated_text;
                translationEl.textContent = savedTranslation;
                playBtn.disabled = false;
            }
        } catch (error) {
            console.error("Error fetching translation:", error);
        }
    }

    // Initialize speech recognition service
    function initSpeechRecognition() {
        if (recognition) recognition.abort();

        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = inputLang.value;
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = (event) => {
            let transcript = "";
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript + " ";
            }

            transcriptEl.textContent = transcript.trim();

            if (transcript.trim() && transcript.trim() !== lastTranscript) {
                lastTranscript = transcript.trim();
                sendTextToAPI(lastTranscript);
            }
        };

        recognition.onerror = (event) => {
            console.error("Speech recognition error:", event.error);
        };

        recognition.onend = () => {
            if (isRecording) {
                console.log("Speech recognition stopped. Restarting...");
                setTimeout(() => recognition.start(), 1000);
            }
        };
    }

    // Handle recording start/stop
    recordBtn.addEventListener("click", () => {
        if (!isRecording) {
            initSpeechRecognition();
            recognition.start();
            isRecording = true;
            recordBtn.textContent = "Stop Speaking";
        } else {
            recognition.stop();
            isRecording = false;
            recordBtn.textContent = "Start Speaking";
        }
    });

    // Play translated text using text-to-speech
    playBtn.addEventListener("click", () => {
        if (savedTranslation) {
            const utterance = new SpeechSynthesisUtterance(savedTranslation);
            utterance.lang = outputLang.value;
            window.speechSynthesis.speak(utterance);
        }
    });

    // Restart speech recognition when the input language changes
    inputLang.addEventListener("change", () => {
        initSpeechRecognition();
    });

    // Initialize speech recognition on page load
    initSpeechRecognition();
});
