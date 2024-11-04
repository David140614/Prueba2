from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegura que el directorio de carga existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return jsonify({"error": "No se subió ningún archivo"}), 400

    file = request.files['audio']
    if file.filename == '':
        return jsonify({"error": "No se seleccionó ningún archivo"}), 400

    # Guarda el archivo
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Simulación de procesamiento de audio
    # Aquí podrías integrar tu modelo de IA para analizar el audio
    result = "Ejemplo: llanto de hambre detectado."

    return jsonify({"message": "Archivo procesado", "result": result})

if __name__ == '__main__':
    app.run(debug=True)
