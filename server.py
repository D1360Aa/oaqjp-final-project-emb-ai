#!/usr/bin/env python3
"""
Servidor Flask para la aplicación de detección de emociones
"""
from flask import Flask, render_template, request, jsonify
import os
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

# Especificar explícitamente la carpeta de templates
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route("/")
def index():
    """
    Ruta principal que renderiza la página HTML
    """
    return render_template('index.html')

@app.route("/emotionDetector", methods=['POST'])
def emotion_detector_route():
    """
    Endpoint para analizar emociones en el texto
    """
    try:
        data = request.get_json()
        
        # Verificar que se recibieron datos JSON
        if not data:
            return jsonify({
                "error": "¡Texto inválido! Por favor, inténtalo de nuevo."
            }), 400
        
        # Verificar que existe el campo 'text'
        if 'text' not in data:
            return jsonify({
                "error": "¡Texto inválido! Por favor, inténtalo de nuevo."
            }), 400
        
        text_to_analyze = data['text']
        
        # Verificar que el texto no esté vacío
        if not text_to_analyze or text_to_analyze.strip() == "":
            return jsonify({
                "error": "¡Texto inválido! Por favor, inténtalo de nuevo."
            }), 400
        
        # Llamar a la función de detección de emociones
        result = emotion_detector(text_to_analyze)
        
        # Verificar si el resultado es válido
        if result is None:
            return jsonify({
                "error": "¡Texto inválido! Por favor, inténtalo de nuevo."
            }), 400
        
        # Verificar si la emoción dominante es None (indicando error)
        if result.get('dominant_emotion') is None:
            return jsonify({
                "error": "¡Texto inválido! Por favor, inténtalo de nuevo."
            }), 400
        
        # Formatear la respuesta exitosa
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
    
    except Exception as e:
        # Manejo de errores inesperados
        print(f"Error interno del servidor: {e}")
        return jsonify({
            "error": "Error interno del servidor. Por favor, inténtalo de nuevo."
        }), 500

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000, debug=True)