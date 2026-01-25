import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

questions = [
    "que es una variable",
    "para que sirve una variable",
    "que es un if",
    "que es un condicional",
    "que es un bucle",
    "que es un ciclo for",
    "que es una funcion",
    "para que sirve una funcion",
    "que es la programacion orientada a objetos",
    "que es una clase",
    "que es python",
    "para que sirve python"
]

answers = [
    "Una variable es un espacio en memoria donde se almacena un valor.",
    "Sirve para guardar información y reutilizarla.",
    "If evalúa una condición y ejecuta un bloque de código.",
    "Un condicional permite tomar decisiones en el programa.",
    "Un bucle permite repetir un bloque de código.",
    "El ciclo for repite instrucciones un número determinado de veces.",
    "Una función es un bloque de código reutilizable.",
    "Las funciones ayudan a organizar el código.",
    "La POO es un paradigma basado en objetos.",
    "Una clase es una plantilla para crear objetos.",
    "Python es un lenguaje de programación fácil de aprender.",
    "Python sirve para desarrollo web, IA y análisis de datos."
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

model = MultinomialNB()
model.fit(X, answers)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Modelo entrenado correctamente")
