# placeholder for ping check
# utils/pingcheck.py

import subprocess
import platform
import time
from utils.storage import load_hosts, save_hosts

def is_online(ip):
    """بررسی فعال بودن IP با ping"""
    count = "1"
    timeout = "1"
    param = "-n" if platform.system().lower() == "windows" else "-c"
    timeout_param = "-w" if platform.system().lower() == "windows" else "-W"

    try:
        result = subprocess.run(
            ["ping", param, count, timeout_param, timeout, ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except Exception:
        return False

def check_all_ping_hosts():
    """بررسی تمام IPهایی که نوع آنها ping است"""
    hosts = load_hosts()
    changed = False

    for host in hosts:
        if host["type"] != "ping":
            continue

        previous_status = host.get("status", "pending")
        current_status = "active" if is_online(host["ip"]) else "down"

        if current_status != previous_status:
            host["status"] = current_status
            changed = True

    if changed:
        save_hosts(hosts)
        print(f"[{time.ctime()}] Ping statuses updated.")
    else:
        print(f"[{time.ctime()}] No ping changes detected.")
