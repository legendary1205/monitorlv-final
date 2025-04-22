# placeholder for storage functions
# utils/storage.py

import json
import os
import uuid

HOSTS_FILE = "data/hosts.json"

def load_hosts():
    """خواندن لیست سرورها از فایل JSON"""
    if not os.path.exists(HOSTS_FILE):
        return []
    try:
        with open(HOSTS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_hosts(hosts):
    """ذخیره لیست سرورها در فایل JSON"""
    with open(HOSTS_FILE, "w") as f:
        json.dump(hosts, f, indent=2, ensure_ascii=False)

def generate_id():
    """ایجاد شناسه یکتا ۸ رقمی"""
    return str(uuid.uuid4())[:8]
