#!/usr/bin/env python3
from flask import Flask, jsonify, abort, send_file, render_template_string
import os
import json
from datetime import datetime

REPORT_DIR = os.path.expanduser("~/remote_reports") 
app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<title>Seahawks Nester</title>
<h1>List of probes (reports)</h1>
<ul>
  {% for f in files %}
    <li><a href="/report/{{ f }}">{{ f }}</a></li>
  {% endfor %}
</ul>
"""

@app.route("/")
def index():
    if not os.path.exists(REPORT_DIR):
        return "No reports dir (server misconfigured)", 500
    files = sorted([f for f in os.listdir(REPORT_DIR) if f.endswith(".json")], reverse=True)
    return render_template_string(TEMPLATE, files=files)

@app.route("/reports")
def list_json():
    files = sorted([f for f in os.listdir(REPORT_DIR) if f.endswith(".json")], reverse=True)
    return jsonify(files)

@app.route("/report/<path:fname>")
def get_report(fname):
    path = os.path.join(REPORT_DIR, fname)
    if not os.path.exists(path):
        abort(404)
    return send_file(path, mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
