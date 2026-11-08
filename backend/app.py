
from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__)

FRONTEND_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)

# Temporary sample data for initial testing
medicines = [
    {"id": 1, "name": "Paracetamol", "quantity": 100},
    {"id": 2, "name": "Cetirizine", "quantity": 50},
    {"id": 3, "name": "Vitamin C", "quantity": 8},
    {"id": 4, "name": "ORS", "quantity": 30}
]


@app.route("/")
def home():
    return send_from_directory(FRONTEND_FOLDER, "index.html")


@app.route("/style.css")
def css():
    return send_from_directory(FRONTEND_FOLDER, "style.css")


@app.route("/script.js")
def javascript():
    return send_from_directory(FRONTEND_FOLDER, "script.js")


@app.route("/api/health")
def health():
    return jsonify({
        "status": "success",
        "message": "NEXORITHAM backend is running"
    })


@app.route("/api/dashboard")
def dashboard():

    total_medicines = len(medicines)

    available_stock = sum(
        medicine["quantity"] for medicine in medicines
    )

    low_stock = sum(
        1 for medicine in medicines
        if medicine["quantity"] < 10
    )

    return jsonify({
        "total_medicines": total_medicines,
        "available_stock": available_stock,
        "low_stock": low_stock,
        "today_sales": 0
    })


@app.route("/api/medicines")
def search_medicines():

    search = request.args.get("search", "").strip().lower()

    results = [
        medicine for medicine in medicines
        if search in medicine["name"].lower()
    ]

    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
