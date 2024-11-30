from pymongo import MongoClient
from flask import Flask, request, render_template, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from bcrypt import hashpw, gensalt
from dotenv import load_dotenv
from datetime import datetime, timezone
from bcrypt import checkpw


load_dotenv()


# Conexión a MongoDB
try:
    client = MongoClient("mongodb+srv://davidzr04:david140614@cluster0.rvnw9.mongodb.net/?retryWrites=true&w=majority")
    db = client["VentaCompraAutopartes"]
    usuarios_collection = db["usuarios"]
    productos_collection = db["productos_publicados"]  # Nueva colección para los productos


except Exception as e:
    print(f"Error conectando a MongoDB: {e}")
    exit(1)

# Función para insertar datos
def registrar_usuario(nombre, email, password):
    try:
        hashed_password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
        usuario = {"nombre": nombre, "email": email, "password": hashed_password}
        usuarios_collection.insert_one(usuario)
        return "Usuario registrado exitosamente."
    except Exception as e:
        return f"Error al registrar usuario: {str(e)}"

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Esto genera una clave secreta para las sesiones

@app.route("/", methods=["GET", "POST"])
def index():

    # Verificar si el usuario está autenticado
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Si el usuario no está autenticado, redirige al login

    if request.method == "POST":
        if 'nombre' in request.form:
            # Registro de usuario
            nombre = request.form["nombre"]
            email = request.form["email"]
            password = request.form["password"]
            mensaje = registrar_usuario(nombre, email, password)
            return render_template("index.html", mensaje=mensaje)

        elif 'nombre_producto' in request.form:
            # Publicación de producto
            nombre_producto = request.form["nombre_producto"]
            descripcion_producto = request.form["descripcion_producto"]
            precio_producto = request.form["precio_producto"]  # Capturar el precio del producto
            imagen_producto = request.files["imagen_producto"]

            # Guardar la imagen en el servidor
            imagen_filename = secure_filename(imagen_producto.filename)
            imagen_path = os.path.join("static/uploads", imagen_filename)
            imagen_producto.save(imagen_path)

            # Insertar el nuevo producto en MongoDB
            nuevo_producto = {
                "nombre_producto": nombre_producto,
                "descripcion_producto": descripcion_producto,
                "precio_producto": float(precio_producto),  # Convertir el precio a un número decimal
                "imagen_producto": imagen_filename,
                "usuario_id": session['user_id'],
                "fecha_publicacion": datetime.now(timezone.utc)
            }

            productos_collection.insert_one(nuevo_producto)
            return redirect(url_for('index'))  # Redirigir a la misma página

    # Obtener todos los productos de MongoDB
    productos = productos_collection.find()
    productos_list = [producto for producto in productos]

    return render_template("index.html", productos=productos_list)

######### Rutas de Login #########

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        usuario = usuarios_collection.find_one({"email": email})
        if usuario and checkpw(password.encode('utf-8'), usuario["password"].encode('utf-8')):
            session['user_id'] = str(usuario['_id'])
            return redirect(url_for('index'))  # Redirigir a la página principal
        else:
            return "Credenciales incorrectas", 401

    return render_template("index.html")  # Mostrar el login en el mismo index

if __name__ == "__main__":
    app.run(debug=True)
