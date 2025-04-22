# placeholder for run_all
# run_all.py

import asyncio
import threading
from monitor_loop import monitor_loop
from bot import main as bot_main
from web.app import app

def run_flask():
    app.run(host="0.0.0.0", port=9000)

async def main():
    # اجرای Flask جداگانه
    threading.Thread(target=run_flask, daemon=True).start()

    # اجرای async هم‌زمان ربات و مانیتور
    await asyncio.gather(
        bot_main(),         # ربات تلگرام
        monitor_loop()      # حلقه مانیتورینگ زنده
    )

if __name__ == "__main__":
    asyncio.run(main())
