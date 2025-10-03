
import os
import json
import time
import socket
import subprocess
from datetime import datetime
import logging
import getpass
import nmap

REPORT_DIR = os.path.expanduser("~/seahawks/reports")
LOG_FILE = os.path.expanduser("~/seahawks/logs/harvester.log")
VERSION_FILE = os.path.expanduser("~/seahawks/VERSION")
NESTER_USER = "seahawks"
NESTER_HOST = "NESTER_IP_OR_HOSTNAME"   
NESTER_REPO_DIR = "/home/seahawks/remote_reports" 
SSH_KEY = os.path.expanduser("~/.ssh/seahawks_harvester_key")  
PING_TARGET = "8.8.8.8"

logger = logging.getLogger("harvester")
logger.setLevel(logging.INFO)
fh = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

def read_version():
    if os.path.exists(VERSION_FILE):
        return open(VERSION_FILE).read().strip()
    return "0.0.0"

def get_hostname_ip():
    hostname = socket.gethostname()
    try:
        ip = subprocess.check_output(["hostname", "-I"]).decode().strip().split()[0]
    except Exception:
        ip = "unknown"
    return hostname, ip

def run_ping(target, count=3, timeout=2):
    try:
        out = subprocess.check_output(["ping", "-c", str(count), "-W", str(timeout), target], stderr=subprocess.DEVNULL).decode()

        for line in out.splitlines():
            if "rtt min/avg" in line or "round-trip" in line:
                parts = line.split("=")[1].strip().split()[0].split("/")
                avg = float(parts[1])
                return avg
    except subprocess.CalledProcessError:
        return None
    except Exception as e:
        logger.exception("ping parse error")
        return None

def discover_hosts(network=None):
    nm = nmap.PortScanner()
    target = network if network else '192.168.1.0/24'  
    try:
        nm.scan(hosts=target, arguments='-sn')
        hosts = []
        for h in nm.all_hosts():
            hosts.append({
                "ip": h,
                "hostname": nm[h].hostname() if 'hostname' in nm[h] else '',
                "state": nm[h].state()
            })
        return hosts
    except Exception:
        logger.exception("nmap failed")
        return []

def make_report():
    ts = datetime.utcnow().isoformat() + "Z"
    hostname, ip = get_hostname_ip()
    version = read_version()
    latency = run_ping(PING_TARGET)
    hosts = discover_hosts()
    report = {
        "generated_at": ts,
        "hostname": hostname,
        "ip": ip,
        "version": version,
        "latency_avg_ms": latency,
        "nb_hosts_detected": len(hosts),
        "hosts": hosts
    }
    return report

def write_report(report):
    os.makedirs(REPORT_DIR, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    hostname = report.get("hostname", "host")
    filename = f"report_{hostname}_{ts}.json"
    path = os.path.join(REPORT_DIR, filename)
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    last = os.path.join(REPORT_DIR, "last_report.json")
    with open(last, "w") as f:
        json.dump(report, f, indent=2)
    return path

def push_to_nester(local_path):
    scp_cmd = ["scp", "-i", SSH_KEY, local_path, f"{NESTER_USER}@{NESTER_HOST}:{NESTER_REPO_DIR}/"]
    try:
        subprocess.check_call(scp_cmd, stderr=subprocess.STDOUT)
        logger.info("Pushed report to nester: %s", local_path)
        return True
    except subprocess.CalledProcessError as e:
        logger.warning("Failed to push to nester (maybe offline): %s", e)
        return False

def main():
    logger.info("Starting harvester run")
    report = make_report()
    path = write_report(report)
    pushed = push_to_nester(path)
    if not pushed:
        logger.info("Report saved locally, will push later when network available.")
    logger.info("Harvester run complete")

if __name__ == "__main__":
    main()
