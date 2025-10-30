# harvester_client.py
import requests, time, argparse, json
from datetime import datetime

def fetch_once(url, timeout=5):
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.json()

def print_and_save(data, out_jsonl=None):
    ts = data.get("ts")
    print(f"[{datetime.utcfromtimestamp(ts).isoformat() if ts else 'no-ts'}] Reçu:")
    print(f"  hostname: {data.get('hostname')}")
    print(f"  ip: {data.get('ip')}")
    print(f"  nb_devices: {data.get('nb_devices')}")
    print(f"  last_scan: {json.dumps(data.get('last_scan'), ensure_ascii=False)}")
    print(f"  wan_latency_ms: {data.get('wan_latency_ms')}")
    print(f"  component_version: {data.get('component_version')}")
    if out_jsonl:
        with open(out_jsonl, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

def run_poll(url, interval=10, out_jsonl=None):
    print("Polling", url, "every", interval, "s")
    while True:
        try:
            data = fetch_once(url)
            print_and_save(data, out_jsonl)
        except Exception as e:
            print(f"[{datetime.utcnow().isoformat()}] Erreur fetch: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="localhost", help="IP/hostname du server (nester)")
    p.add_argument("--port", default=5000, type=int, help="port du serveur")
    p.add_argument("--interval", default=10, type=int, help="intervalle de polling en secondes")
    p.add_argument("--out-jsonl", default=None, help="fichier JSONL pour append des mesures")
    args = p.parse_args()

    url = f"http://{args.host}:{args.port}/data"
    run_poll(url, args.interval, args.out_jsonl)






























































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
