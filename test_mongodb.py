from pymongo import MongoClient

# Reemplaza con tu URI
uri = "mongodb+srv://davidzr04:david140614@cluster0.rvnw9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
try:
    client = MongoClient(uri)
    print("Conexión exitosa a MongoDB")
except Exception as e:
    print(f"Error conectando a MongoDB: {e}")
