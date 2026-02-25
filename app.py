from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)


# -------------------------
# DATABASE INITIALIZATION
# -------------------------

def init_db():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            score INTEGER,
            risk TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


# -------------------------
# ANALYZE ROUTE
# -------------------------

@app.route("/analyze", methods=["POST"])
def analyze_job():
    data = request.get_json()
    text = data.get("text", "").lower()

    score = 100
    flags = []

    # 🔴 Strong Scam Indicators
    strong_scam = [
        "registration fee",
        "internship fee",
        "security deposit",
        "pay amount"
    ]

    # 🟠 Psychological Pressure
    pressure_phrases = [
        "limited slots",
        "confirm your seat",
        "immediate openings",
        "interview process almost over",
        "short-listed"
    ]

    # 🟡 MLM / Marketing Style Signals
    mlm_style = [
        "managerial position",
        "entrepreneurship",
        "global training module",
        "rapid promotion",
        "business development associate"
    ]

    # 📧 Free email domains
    free_domains = ["gmail.com", "yahoo.com", "outlook.com"]

    # ---- CATEGORY CHECKS ----

    matched_strong = [word for word in strong_scam if word in text]
    if matched_strong:
        score -= 25
        flags.append("Strong scam indicator detected 🚩")

    matched_pressure = [word for word in pressure_phrases if word in text]
    if matched_pressure:
        score -= 10
        flags.append("Uses urgency / pressure tactics 🚩")

    matched_mlm = [word for word in mlm_style if word in text]
    if matched_mlm:
        score -= 5
        flags.append("Marketing/MLM-style language detected 🚩")

    matched_domains = [domain for domain in free_domains if domain in text]
    if matched_domains:
        score -= 10
        flags.append("Uses free email domain 🚩")

    # ---- FINAL CLASSIFICATION ----

    if score >= 80:
        risk = "Low"
    elif score >= 50:
        risk = "Medium"
    else:
        risk = "High"

    # ---- SAVE TO DATABASE ----

    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO history (text, score, risk, created_at)
        VALUES (?, ?, ?, ?)
    """, (text, score, risk, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()
    matched_words = matched_strong + matched_pressure + matched_mlm
    return jsonify({
    "score": max(score, 0),
    "risk": risk,
    "flags": flags,
    "matched_words": matched_words
})

# -------------------------
# HISTORY ROUTE
# -------------------------

@app.route("/history", methods=["GET"])
def get_history():
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, score, risk, created_at FROM history ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()

    history = []
    for row in rows:
        history.append({
            "id": row[0],
            "score": row[1],
            "risk": row[2],
            "created_at": row[3]
        })

    return jsonify(history)

@app.route("/history/<int:item_id>", methods=["DELETE"])
def delete_history(item_id):
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM history WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted successfully"})    


# -------------------------
# RUN SERVER
# ------------------------
import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))