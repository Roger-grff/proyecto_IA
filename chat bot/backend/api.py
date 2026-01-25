from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os
import re
import unicodedata

def limpiar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

app = Flask(__name__)
CORS(app)  # 👈 ESTO SOLUCIONA EL PROBLEMA

# Verificación de modelo
if not os.path.exists("model.pkl") or not os.path.exists("vectorizer.pkl"):
    raise Exception("Ejecuta train_model.py primero")

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = limpiar_texto(data.get("message", ""))

    X = vectorizer.transform([user_message])
    probs = model.predict_proba(X)
    confidence = np.max(probs)

    confidence = np.max(probs)
    print("Confianza:", confidence)

    if confidence < 0.12:
        return jsonify({
            "response": "No tengo información sobre ese tema todavía."
        })

    response = model.predict(X)[0]
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

