# send_report.py
#!/usr/bin/env python3
import requests, socket, os, subprocess, re, time

NESTER = os.environ.get("NESTER_URL", "http://192.168.56.103:5000")
TARGET = NESTER.rstrip("/") + "/api/report"
HARVESTER_IP = os.environ.get("HARVESTER_IP")

def my_ip_for(target_ip, target_port=80):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((target_ip, target_port))
        return s.getsockname()[0]
    finally:
        s.close()

def ip_from_interfaces(candidates=("enp0s8","enp0s3","ens33","eth0")):
    for iface in candidates:
        try:
            out = subprocess.check_output(["ip","-4","addr","show",iface], text=True, stderr=subprocess.DEVNULL)
            m = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)", out)
            if m: return m.group(1)
        except Exception:
            pass
    return None

def avg_ping_ms(target_ip):
    try:
        out = subprocess.check_output(["ping","-c","3", target_ip], text=True, stderr=subprocess.DEVNULL)
        m = re.search(r"= .*?/([\d\.]+)/", out)
        return float(m.group(1)) if m else None
    except Exception:
        return None

def main():
    node = socket.gethostname()
    nester_ip = NESTER.split("://",1)[-1].split("/",1)[0].split(":")[0]
    ip = HARVESTER_IP or my_ip_for(nester_ip) or ip_from_interfaces() or ""
    latency = avg_ping_ms(nester_ip) or 0.0
    payload = {"node": node, "ip": ip, "devices": 0, "latency_ms": latency}
    try:
        r = requests.post(TARGET, json=payload, timeout=5)
        print(time.strftime("%F %T"), r.status_code, r.text)
    except Exception as e:
        print("error:", e)

if __name__ == "__main__":
    main()
