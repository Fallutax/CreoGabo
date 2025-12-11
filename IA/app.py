from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Agregar la ruta de src al PYTHONPATH
src_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "Proyecto_inteligencia_artificial_productos_quimicos", "src")
)
if src_path not in sys.path:
    sys.path.append(src_path)

try:
    from main import ChemicalAssistant, AppConfig
except ImportError as e:
    raise ImportError(f"Error al importar 'main.py': {e}. Verifica la ruta y el archivo.")

app = Flask(__name__)
CORS(app)  # ✅ Habilitar CORS

# Inicializar el asistente una sola vez
assistant = ChemicalAssistant(AppConfig())

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("question", "")
    if not query:
        return jsonify({"error": "No se envió ninguna pregunta"}), 400
    
    respuesta, fuentes = assistant.ask(query)
    return jsonify({
        "answer": respuesta,
        "sources": [f.metadata for f in fuentes] if fuentes else []
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)