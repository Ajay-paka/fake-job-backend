from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

from analyzer import analyze_text
from database import get_db_connection, init_db

app = Flask(__name__)
CORS(app)

init_db()


# -------------------------
# ANALYZE ROUTE
# -------------------------

@app.route("/analyze", methods=["POST"])
def analyze_job():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Invalid request"}), 400

    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Text cannot be empty"}), 400

    result = analyze_text(text)

    # Save to DB
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO history (text, score, risk, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        text.lower(),
        result["score"],
        result["risk"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return jsonify(result)


# -------------------------
# HISTORY ROUTE
# -------------------------

@app.route("/history", methods=["GET"])
def get_history():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, score, risk, created_at FROM history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    history = [
        {
            "id": row["id"],
            "score": row["score"],
            "risk": row["risk"],
            "created_at": row["created_at"]
        }
        for row in rows
    ]

    return jsonify(history)


@app.route("/history/<int:item_id>", methods=["DELETE"])
def delete_history(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM history WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted successfully"})


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))