from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import torch
import unicodedata
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ------------------------------
# Función para limpiar texto
# ------------------------------
def limpiar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

# ------------------------------
# Inicializar app
# ------------------------------
app = Flask(__name__)
CORS(app)

# ------------------------------
# Cargar datos entrenados
# ------------------------------
with open("questions.pkl", "rb") as f:
    questions = pickle.load(f)
with open("answers.pkl", "rb") as f:
    answers = pickle.load(f)
with open("embeddings.pkl", "rb") as f:
    question_embeddings = pickle.load(f)

# Modelo de embeddings
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# ------------------------------
# Endpoint chat
# ------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = limpiar_texto(data.get("message", ""))

    # Crear embedding de la pregunta del usuario
    user_emb = embedder.encode([user_message], convert_to_tensor=True)

    # Calcular similitud coseno
    similarities = cosine_similarity(user_emb, question_embeddings.cpu().numpy())
    best_idx = int(np.argmax(similarities))

    confidence = float(np.max(similarities))

    # Si similitud baja, respuesta por defecto
    if confidence < 0.4:  # Ajustable según necesites
        return jsonify({"response": "No tengo información sobre ese tema todavía.", "confidence": round(confidence,2)})

    # Asegurar que el índice no se salga de rango
    if best_idx >= len(answers):
        return jsonify({"response": "No tengo información sobre ese tema todavía.", "confidence": round(confidence,2)})

    response = answers[best_idx]
    return jsonify({"response": response, "confidence": round(confidence,2)})

# ------------------------------
# Ejecutar app
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
