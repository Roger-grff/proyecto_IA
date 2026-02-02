from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import numpy as np
import unicodedata
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import sys
import webbrowser
import threading
import time

# ------------------------------
# Utilidades del chat bot
# ------------------------------
def limpiar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ------------------------------
# Flask
# ------------------------------
app = Flask(__name__, static_folder=None)
CORS(app)

# ------------------------------
# Frontend path
# ------------------------------
FRONTEND_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)

# ------------------------------
# Cargar IA
# ------------------------------
with open(resource_path("questions.pkl"), "rb") as f:
    questions = pickle.load(f)

with open(resource_path("answers.pkl"), "rb") as f:
    answers = pickle.load(f)

with open(resource_path("embeddings.pkl"), "rb") as f:
    question_embeddings = pickle.load(f)

embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------------------
# RUTAS FRONTEND
# ------------------------------
@app.route("/")
def index():
    return send_from_directory(FRONTEND_PATH, "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_PATH, filename)

# ------------------------------
# API CHAT
# ------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = limpiar_texto(data.get("message", ""))

    user_emb = embedder.encode([user_message], convert_to_tensor=True)
    similarities = cosine_similarity(
        user_emb, question_embeddings.cpu().numpy()
    )

    best_idx = int(np.argmax(similarities))
    confidence = float(np.max(similarities))

    if confidence < 0.60 or best_idx >= len(answers):
        return jsonify({
            "response": "No tengo información sobre ese tema todavía.",
            "confidence": round(confidence, 2)
        })

    return jsonify({
        "response": answers[best_idx],
        "confidence": round(confidence, 2)
    })

# ------------------------------
# Abrir navegador
# ------------------------------
def abrir_frontend():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:5000")

# ------------------------------
# Main
# ------------------------------
if __name__ == "__main__":
    threading.Thread(target=abrir_frontend, daemon=True).start()
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

