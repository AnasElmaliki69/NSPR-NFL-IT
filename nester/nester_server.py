
# nester_server.py
from flask import Flask, jsonify, request
import socket, time, json, os, random, subprocess, shutil, statistics

app = Flask(__name__)

# --- Helpers ---
def get_hostname():
    return socket.gethostname()

def get_primary_ip():
    """Trick: create UDP socket to a public ip to get local interface IP (no packet sent)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # fallback: hostname -> ip
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return None

def count_devices_from_file(path="devices.json"):
    """Si devices.json existe et contient une liste d'objets, retourne len(list)."""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return len(data)
            # si c'est un dict avec key 'devices'
            if isinstance(data, dict) and "devices" in data and isinstance(data["devices"], list):
                return len(data["devices"])
        except Exception:
            pass
    # sinon simulation
    return random.randint(0, 20)

def read_last_scan(path="last_scan.json"):
    """Retourne le JSON du dernier scan si disponible, sinon un mock simple."""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # mock
    return {
        "status": "ok",
        "found": ["deviceA", "deviceB"] if random.random() > 0.4 else [],
        "notes": "simulated"
    }

def read_component_version(path="component_version.txt"):
    if os.path.exists(path):
        try:
            v = open(path, "r", encoding="utf-8").read().strip()
            return v or None
        except Exception:
            pass
    # mock
    return "v1.0.0-sim"

def ping_avg_ms(host="8.8.8.8", count=4, timeout_s=2):
    """Try system ping (unix). If not available or fails, fallback to TCP connect timings."""
    ping_bin = shutil.which("ping")
    if ping_bin:
        # build ping command for unix-like (Mac/Linux)
        cmd = [ping_bin, "-c", str(count), "-W", str(timeout_s), host]
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True, timeout=(count*timeout_s + 5))
            # parse avg from output line like: rtt min/avg/max/mdev = 9.370/9.370/9.370/0.000 ms
            for line in out.splitlines():
                if "rtt min" in line or "round-trip" in line or "rtt " in line:
                    try:
                        # extract the part after '='
                        parts = line.split("=")[1].strip().split()[0]
                        # parts like min/avg/max/mdev
                        avg = parts.split("/")[1]
                        return float(avg)
                    except Exception:
                        continue
        except Exception:
            pass
    # fallback: measure TCP connect time to host:53 (DNS) multiple times
    times = []
    for i in range(max(1, count)):
        try:
            t0 = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout_s)
            s.connect((host, 53))
            s.close()
            times.append((time.time() - t0) * 1000.0)
        except Exception:
            # record a large value to indicate timeout, but avoid skewing too much
            times.append(timeout_s * 1000.0)
    try:
        return round(statistics.mean(times), 2)
    except Exception:
        return None

@app.route("/data", methods=["GET"])
def data():
    harvester_ip = request.remote_addr
    res = {
        "ts": int(time.time()),
        "hostname": get_hostname(),      
        "nester_ip": get_primary_ip(),   
        "harvester_ip": harvester_ip,
        "nb_devices": count_devices_from_file(),
        "last_scan": read_last_scan(),
        "wan_latency_ms": ping_avg_ms(),
        "component_version": read_component_version()
    }
    return jsonify(res)

@app.route("/", methods=["GET"])
def index():
    return "<h3>Nester server — GET /data to retrieve JSON metrics (hostname, ip, nb_devices, last_scan, wan_latency_ms, component_version)</h3>"

if __name__ == "__main__":
    # écoute sur toutes les interfaces
    app.run(host="0.0.0.0", port=5000, debug=True)

