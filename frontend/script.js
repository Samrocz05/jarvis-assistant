// Function to play sound
function playSound(filename) {
    const audio = new Audio(`frontend/assets/sounds/${filename}`);  // Updated path
    audio.play();
}

// Initialize speech synthesis
const synth = window.speechSynthesis;

// Function to speak text
function speakText(text) {
    // Create a new SpeechSynthesisUtterance
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US'; // Adjust language if needed

    // Check if there's already something being spoken
    if (synth.speaking) {
        // Queue up the new utterance
        synth.addEventListener('end', () => {
            synth.speak(utterance);
        });
    } else {
        // Speak immediately if nothing else is being spoken
        synth.speak(utterance);
    }
}

// Event listener for submitting text input
document.getElementById('submit-btn').addEventListener('click', () => {
    const input = document.getElementById('input-text').value;
    if (input.trim() === "") {
        const errorMsg = "Please enter a command.";
        document.getElementById('response').innerText = errorMsg;
        playSound('error_alert.mp3');
        speakText(errorMsg);
        return;
    }
    
    playSound('futuristic_ui_click.mp3');

    if (input.toLowerCase().includes('yes')) {
        playSound('yes_sir_response.mp3');
    }
    
    fetch('http://127.0.0.1:5000/generate', {  // Update URL to your Flask backend
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: input })
    })
    .then(response => response.json())
    .then(data => {
        const responseText = data.generated_text;  // Adjust based on backend response
        document.getElementById('response').innerText = responseText;
        playSound('task_success.mp3');
        speakText(responseText);
    })
    .catch(() => {
        const errorMsg = "An error occurred.";
        document.getElementById('response').innerText = errorMsg;
        playSound('error_alert.mp3');
        speakText(errorMsg);
    });
});

// Example usage of speech synthesis
const utterance1 = new SpeechSynthesisUtterance("How about we say this now? This is quite a long sentence to say.");
const utterance2 = new SpeechSynthesisUtterance("We should say another sentence too, just to be on the safe side.");

// Speak the sentences one after another
synth.speak(utterance1);
synth.speak(utterance2);

// Optional: Play startup sound on page load
window.onload = () => {
    playSound('jarvis_startup.mp3');
};

// Optional: Play shutdown sound when the user closes the page
window.onbeforeunload = () => {
    playSound('shutdown_goodbye.mp3');
};
