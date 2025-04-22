# placeholder for Flask app# web/app.py

from flask import Flask, render_template
import json
import os

app = Flask(__name__, template_folder="templates")
DATA_FILE = os.path.join("data", "hosts.json")

def load_hosts():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

@app.route("/")
def status_page():
    hosts = load_hosts()
    ping = [h for h in hosts if h["type"] == "ping"]
    traffic = [h for h in hosts if h["type"] == "traffic"]
    bandwidth = [h for h in hosts if h["type"] == "bandwidth"]

    return render_template("status.html", ping=ping, traffic=traffic, bandwidth=bandwidth)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
