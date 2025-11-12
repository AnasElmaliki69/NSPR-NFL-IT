# app.py
from flask import Flask, jsonify, request, render_template
from datetime import datetime
import json, os, threading

app = Flask(__name__, template_folder="templates")
BASE = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE, "data.json")
_lock = threading.Lock()

def load_reports():
    if not os.path.exists(DATA_PATH):
        return {}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_reports(reports):
    tmp = DATA_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(reports, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DATA_PATH)

reports = load_reports()

@app.route("/")
def index():
    with _lock:
        current = dict(reports)
    return render_template("index.html", reports=current)

@app.route("/api/report", methods=["POST"])
def receive_report():
    data = request.get_json(force=True)
    node = data.get("node", "unknown")
    data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with _lock:
        reports[node] = data
        save_reports(reports)
    return jsonify({"status":"ok","received_for":node}), 201

@app.route("/api/reports", methods=["GET"])
def list_reports():
    with _lock:
        current = dict(reports)
    return jsonify(current)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
