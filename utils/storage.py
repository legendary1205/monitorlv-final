import json
import os
import uuid

HOSTS_FILE = "data/hosts.json"

def load_hosts():
    if not os.path.exists(HOSTS_FILE):
        return []
    with open(HOSTS_FILE, "r") as f:
        return json.load(f)

def save_hosts(hosts):
    os.makedirs("data", exist_ok=True)
    with open(HOSTS_FILE, "w") as f:
        json.dump(hosts, f, indent=2, ensure_ascii=False)

def generate_id():
    return str(uuid.uuid4())[:8]
