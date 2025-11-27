// Emotion Detection Web Application
console.log("Emotion Detection Web App Loaded");

function clearText() {
    document.getElementById('textToAnalyze').value = '';
    document.getElementById('result').innerHTML = '';
}

// Función adicional para mejorar la UX
function handleKeyPress(event) {
    if (event.key === 'Enter' && event.ctrlKey) {
        analyzeEmotion();
    }
}
