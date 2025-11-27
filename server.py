"""
Servidor Flask para la aplicación de detección de emociones.
Módulo principal que despliega la interfaz web para análisis de emociones.
"""

import os
from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector

# Configurar Flask con carpeta de templates explícita
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)


@app.route("/")
def index():
    """
    Ruta principal que renderiza la página HTML de la aplicación.
    
    Returns:
        str: HTML de la página principal de detección de emociones.
    """
    return render_template('index.html')


@app.route("/emotionDetector", methods=['POST'])
def emotion_detector_route():
    """
    Endpoint REST para analizar emociones en texto mediante Watson NLP.
    
    Returns:
        JSON: Resultado del análisis emocional o mensaje de error.
    """
    # Validar datos de entrada
    if not request.get_json() or 'text' not in request.get_json():
        return jsonify({
            "error": "¡Texto inválido! Por favor, inténtalo de nuevo."
        }), 400

    data = request.get_json()
    text_to_analyze = data['text']

    # Validar texto no vacío
    if not text_to_analyze or text_to_analyze.strip() == "":
        return jsonify({
            "error": "¡Texto inválido! Por favor, inténtalo de nuevo."
        }), 400

    # Ejecutar análisis de emociones
    result = emotion_detector(text_to_analyze)

    # Validar resultado
    if result is None or result.get('dominant_emotion') is None:
        return jsonify({
            "error": "¡Texto inválido! Por favor, inténtalo de nuevo."
        }), 400

    # Formatear respuesta exitosa
    response_text = (
        f"Para la declaración dada, la respuesta del sistema es "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} y "
        f"'sadness': {result['sadness']}. "
        f"La emoción dominante es {result['dominant_emotion']}."
    )

    return jsonify({
        "anger": result['anger'],
        "disgust": result['disgust'],
        "fear": result['fear'],
        "joy": result['joy'],
        "sadness": result['sadness'],
        "dominant_emotion": result['dominant_emotion'],
        "response_text": response_text
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
