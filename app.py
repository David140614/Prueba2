from pymongo import MongoClient
from flask import Flask, request, render_template, redirect, url_for
import os
from bcrypt import hashpw, gensalt
from dotenv import load_dotenv
load_dotenv()


# Conexión a MongoDB
try:
    client = MongoClient("mongodb+srv://davidzr04:david140614@cluster0.rvnw9.mongodb.net/?retryWrites=true&w=majority")
    db = client["VentaCompraAutopartes"]
    collection = db["usuarios"]

except Exception as e:
    print(f"Error conectando a MongoDB: {e}")
    exit(1)

# Función para insertar datos
def registrar_usuario(nombre, email, password):
    try:
        hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
        usuario = {"nombre": nombre, "email": email, "password": hashed_password}
        print(f"Intentando guardar en MongoDB: {usuario}")  # Agrega este print
        collection.insert_one(usuario)
        print("Usuario guardado exitosamente.")
        return "Usuario registrado exitosamente."
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return f"Error al registrar usuario: {str(e)}"


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit-form", methods=["POST"])
def submit_form():
    nombre = request.form["nombre"]
    email = request.form["email"]
    password = request.form["password"]
    mensaje = registrar_usuario(nombre, email, password)
    return render_template("index.html", mensaje=mensaje)

if __name__ == "__main__":
    app.run(debug=True)
