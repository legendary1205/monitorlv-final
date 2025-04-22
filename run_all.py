# run_all.py

import asyncio
import threading
from monitor_loop import monitor_loop
from bot import main as run_bot
from web.app import app

def run_flask():
    app.run(host="0.0.0.0", port=9000)

def run_all():
    # Flask در thread جدا
    threading.Thread(target=run_flask, daemon=True).start()

    # اجرای ربات به صورت sync
    threading.Thread(target=run_bot, daemon=True).start()

    # مانیتورینگ async
    asyncio.run(monitor_loop())

if __name__ == "__main__":
    run_all()
