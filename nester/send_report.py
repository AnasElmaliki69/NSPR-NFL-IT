#!/usr/bin/env python3
import requests, socket, subprocess, re, json, os, time

NESTER = os.environ.get("NESTER_URL", "http://192.168.56.103:5000")  # change if needed
TARGET = NESTER.rstrip("/") + "/api/report"

def hostname():
    return socket.gethostname()

def my_ip():
    # quick method: parse ip from ip command for primary interface enp0s8
    try:
        out = subprocess.check_output(["ip","-4","addr","show","enp0s8"], text=True)
        m = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)", out)
        if m: return m.group(1)
    except Exception:
        pass
    return None

def avg_ping_ms(target_ip):
    try:
        out = subprocess.check_output(["ping","-c","3", target_ip], text=True, stderr=subprocess.DEVNULL)
        m = re.search(r"= .*?/([\d\.]+)/", out)
        if m: return float(m.group(1))
    except Exception:
        return None

def count_devices_cidr(cidr="192.168.56.0/24"):
    # optional: requires nmap installed; returns number of hosts up
    try:
        out = subprocess.check_output(["nmap","-sn", cidr], text=True)
        return out.count("Nmap scan report for")
    except Exception:
        return -1

def main():
    node = hostname()
    ip = my_ip() or ""
    latency = avg_ping_ms("192.168.56.103") or 0.0
    devices = count_devices_cidr()  # may return -1 if nmap missing
    payload = {
        "node": node,
        "ip": ip,
        "devices": devices,
        "latency_ms": latency
    }
    try:
        r = requests.post(TARGET, json=payload, timeout=5)
        print(r.status_code, r.text)
    except Exception as e:
        print("error:", e)

if __name__ == "__main__":
    main()
