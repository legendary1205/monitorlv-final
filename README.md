# monitorlv

💠 **monitorlv** is a live monitoring system that combines a Telegram bot and a web dashboard to track server health via:

- 🟢 **Ping**
- 📊 **Traffic reachability**
- 📡 **Bandwidth usage (via SNMP)**

---

## 📦 Features

- 🎛 Telegram bot with inline control panel
- 🌐 Web interface with sky-blue and white theme
- 🔔 Real-time alerts in Telegram group
- 🧠 Live status tracking with periodic auto-check
- 📋 JSON-based config (no DB needed)
- ✅ Admin-only access control

---

## 🔧 Installation (Ubuntu)

```bash
git clone https://github.com/yourusername/monitorlv.git
cd monitorlv
chmod +x install.sh
./install.sh
python3 run_all.py
```


❌ حذف	Remove a monitored server
📋 لیست	View all monitored servers

---
🖥 Web UI
Runs on: http://yourserver:9000

✅ Green = Active

⚠️ Yellow = Pending

❌ Red = Down
---

📁 Project Structure
```bash
monitorlv/
│
├── bot.py              # Starts Telegram bot
├── monitor_loop.py     # Real-time monitoring loop
├── run_all.py          # Runs everything together
│
├── handlers/           # Bot panel, ping, traffic, bandwidth
├── utils/              # SNMP, pingcheck, storage
├── web/                # Flask web app
├── data/hosts.json     # Server list
│
├── install.sh
├── requirements.txt
├── config.py
└── README.md
📜 License
MIT License — do what you want 😉

```