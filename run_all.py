import asyncio
import threading
from monitor_loop import monitor_loop
from bot import run_bot
from web.app import app

def run_flask():
    app.run(host="0.0.0.0", port=9000)

async def main():
    threading.Thread(target=run_flask, daemon=True).start()

    await asyncio.gather(
        run_bot(),
        monitor_loop()
    )

if __name__ == "__main__":
    asyncio.run(main())