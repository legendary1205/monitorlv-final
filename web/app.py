from flask import Flask, render_template, request, redirect, url_for
import json
import os
import uuid

app = Flask(__name__)
HOSTS_FILE = "data/hosts.json"

# 📦 تابع‌های کمکی برای فایل JSON
def load_hosts():
    if not os.path.exists(HOSTS_FILE):
        return []
    with open(HOSTS_FILE, "r") as f:
        return json.load(f)

def save_hosts(hosts):
    with open(HOSTS_FILE, "w") as f:
        json.dump(hosts, f, ensure_ascii=False, indent=2)

# 🧑‍💻 پنل کاربر
@app.route("/")
def user_panel():
    hosts = load_hosts()
    return render_template("user.html", hosts=hosts)

# 🔐 پنل مدیریت
@app.route("/admin")
def admin_panel():
    hosts = load_hosts()
    return render_template("admin.html", hosts=hosts)

# ➕ افزودن سرور از فرم مدیریت
@app.route("/admin/add", methods=["POST"])
def admin_add():
    ip = request.form.get("ip")
    hostname = request.form.get("hostname")
    type_ = request.form.get("type")

    new_host = {
        "id": uuid.uuid4().hex[:8],
        "ip": ip,
        "hostname": hostname,
        "type": type_,
        "status": "pending"
    }

    hosts = load_hosts()
    hosts.append(new_host)
    save_hosts(hosts)

    return redirect(url_for("admin_panel"))

# 🗑 حذف سرور از مدیریت
@app.route("/admin/delete", methods=["POST"])
def admin_delete():
    host_id = request.form.get("id")
    hosts = load_hosts()
    hosts = [h for h in hosts if h["id"] != host_id]
    save_hosts(hosts)

    return redirect(url_for("admin_panel"))

# 🏁 اجرا
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
