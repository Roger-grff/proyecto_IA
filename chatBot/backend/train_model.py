import pickle
from sentence_transformers import SentenceTransformer
import unicodedata
import re

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
# LISTA DE PREGUNTAS (variaciones) Y RESPUESTAS
# ------------------------------

questions = [
    # NUEVAS PREGUNTAS QUE ME DISTE
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
    "para que sirve python",

    # VARIACIONES DE LOS CONCEPTOS (3 por concepto)
    # VARIABLES
    "explica variable","q es una varible","uso de variable",
    "para que se usan las variables","como se declara una variable","ejemplo de variable",

    # TIPOS DE DATOS
    "que es un tipo de dato","explica tipos de datos","cuales son los tipos de datos",
    "tipos de variables en python","que tipos de variables existen","tipos de datos en python",

    # CONDICIONALES
    "como funciona if","explica condicional if","cuando usar if",
    "que es un else","explica else","para que sirve else",
    "que es elif","explica elif","cuando usar elif",

    # BUCLES
    "que es un bucle","explica un ciclo","que es un ciclo for",
    "que es while","explica ciclo while","como funciona while",

    # FUNCIONES
    "como crear una funcion","ejemplo de funcion en python","definir funcion",
    "para que se usan las funciones","beneficios de funciones","funciones reutilizables",

    # POO
    "explica clase","que es un objeto","que es un metodo",
    "explica metodo","para que sirve un metodo","como usar herencia",
    "explica herencia","que es encapsulamiento","explica polimorfismo",

    # ESTRUCTURAS DE DATOS
    "que es una lista","explica lista en python","que es un arreglo",
    "que es un diccionario","explica diccionario","para que sirve un diccionario",
    "que es una tupla","explica tupla","para que sirve una tupla",
    "que es un set","explica set","para que sirve set",

    # PROGRAMACION TEORICA
    "que es la programacion","explica programacion","definicion de programacion",
    "cuales son los paradigmas de programacion","explica paradigmas","tipos de paradigmas en programacion",
    "que es un algoritmo","explica algoritmo","ejemplo de algoritmo en python",
    "quien creo python","historia de python","origen de python",
    "cuales son las buenas practicas de programacion","explica buenas practicas","como escribir codigo limpio"
]

# RESPUESTAS (una por concepto)
answers = [
    # NUEVAS PREGUNTAS QUE ME DISTE
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
    "Python sirve para desarrollo web, IA y análisis de datos.",

    # VARIACIONES - se asigna la misma respuesta por grupo
    "Una variable es un espacio en memoria donde se almacena un valor.",
    "Una variable es un espacio en memoria donde se almacena un valor.",
    "Una variable es un espacio en memoria donde se almacena un valor.",
    "Sirve para guardar información y reutilizarla.",
    "Sirve para guardar información y reutilizarla.",
    "Sirve para guardar información y reutilizarla.",

    "Tipos de datos: int, float, str, bool, list, tuple, dict, set.",
    "Tipos de datos: int, float, str, bool, list, tuple, dict, set.",
    "Tipos de datos: int, float, str, bool, list, tuple, dict, set.",
    "Tipos de datos: int, float, str, bool, list, tuple, dict, set.",
    "Tipos de datos: int, float, str, bool, list, tuple, dict, set.",
    "Tipos de datos: int, float, str, bool, list, tuple, dict, set.",

    "If evalúa una condición y ejecuta un bloque de código.",
    "If evalúa una condición y ejecuta un bloque de código.",
    "If evalúa una condición y ejecuta un bloque de código.",
    "Else se ejecuta si la condición del if es falsa.",
    "Else se ejecuta si la condición del if es falsa.",
    "Else se ejecuta si la condición del if es falsa.",
    "El elif se usa para múltiples condiciones en un if.",
    "El elif se usa para múltiples condiciones en un if.",
    "El elif se usa para múltiples condiciones en un if.",

    "Un bucle permite repetir un bloque de código.",
    "Un bucle permite repetir un bloque de código.",
    "El ciclo for repite instrucciones un número determinado de veces.",
    "While repite instrucciones mientras se cumpla la condición.",
    "While repite instrucciones mientras se cumpla la condición.",
    "While repite instrucciones mientras se cumpla la condición.",

    "Una función es un bloque de código reutilizable.",
    "Una función es un bloque de código reutilizable.",
    "Una función es un bloque de código reutilizable.",
    "Las funciones ayudan a organizar el código.",
    "Las funciones ayudan a organizar el código.",
    "Las funciones ayudan a organizar el código.",

    "Clase: plantilla para crear objetos.",
    "Objeto: instancia de una clase.",
    "Método: función dentro de una clase.",
    "Método: función dentro de una clase.",
    "Método: función dentro de una clase.",
    "Herencia permite reutilizar atributos/métodos de otra clase.",
    "Herencia permite reutilizar atributos/métodos de otra clase.",
    "Encapsulamiento oculta datos internos de la clase.",
    "Polimorfismo permite que un mismo método tenga distintos comportamientos.",

    "Lista: colección ordenada de elementos.",
    "Lista: colección ordenada de elementos.",
    "Lista: colección ordenada de elementos.",
    "Diccionario: pares clave-valor.",
    "Diccionario: pares clave-valor.",
    "Diccionario: pares clave-valor.",
    "Tupla: colección inmutable.",
    "Tupla: colección inmutable.",
    "Tupla: colección inmutable.",
    "Set: colección sin duplicados.",
    "Set: colección sin duplicados.",
    "Set: colección sin duplicados.",

    "Programación: proceso de crear instrucciones que una computadora pueda ejecutar.",
    "Programación: proceso de crear instrucciones que una computadora pueda ejecutar.",
    "Programación: proceso de crear instrucciones que una computadora pueda ejecutar.",
    "Paradigmas de programación: Imperativo, Declarativo, Funcional, POO.",
    "Paradigmas de programación: Imperativo, Declarativo, Funcional, POO.",
    "Paradigmas de programación: Imperativo, Declarativo, Funcional, POO.",
    "Algoritmo: pasos ordenados para resolver un problema.",
    "Algoritmo: pasos ordenados para resolver un problema.",
    "Algoritmo: pasos ordenados para resolver un problema.",
    "Python fue creado por Guido van Rossum en 1991.",
    "Python fue creado por Guido van Rossum en 1991.",
    "Python fue creado por Guido van Rossum en 1991.",
    "Buenas prácticas: escribir código limpio, legible y modular.",
    "Buenas prácticas: escribir código limpio, legible y modular.",
    "Buenas prácticas: escribir código limpio, legible y modular."
]

# ------------------------------
# Limpiar preguntas
# ------------------------------
questions_clean = [limpiar_texto(q) for q in questions]

# ------------------------------
# Crear embeddings
# ------------------------------
embedder = SentenceTransformer('all-MiniLM-L6-v2')
question_embeddings = embedder.encode(questions_clean, convert_to_tensor=True)

# ------------------------------
# Guardar datos
# ------------------------------
with open("questions.pkl", "wb") as f:
    pickle.dump(questions, f)
with open("answers.pkl", "wb") as f:
    pickle.dump(answers, f)
with open("embeddings.pkl", "wb") as f:
    pickle.dump(question_embeddings, f)

print("Dataset entrenado y embeddings guardados correctamente")
