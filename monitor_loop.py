# monitor_loop.py

import asyncio
import subprocess
from utils.storage import load_hosts, save_hosts
from config import GROUP_ID
from telegram import Bot
from config import BOT_TOKEN
import datetime

last_status = {}

async def monitor_loop():
    while True:
        hosts = load_hosts()
        updated = False

        for host in hosts:
            if host["type"] != "ping":
                continue

            ip = host["ip"]
            hostname = host["hostname"]
            host_id = host["id"]
            current = ping_host(ip)
            previous = last_status.get(host_id, "unknown")

            if current != previous:
                updated = True
                await notify_change(ip, hostname, previous, current)
                for h in hosts:
                    if h["id"] == host_id:
                        h["status"] = current
                last_status[host_id] = current

        if updated:
            save_hosts(hosts)

        print(f"[{datetime.datetime.now().strftime('%c')}] بدون تغییر در وضعیت.")
        await asyncio.sleep(30)

def ping_host(ip):
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "1", ip], stderr=subprocess.DEVNULL)
        return "فعال"
    except subprocess.CalledProcessError:
        return "غیرفعال"

async def notify_change(ip, hostname, old, new):
    bot = Bot(token=BOT_TOKEN)
    if new == "غیرفعال":
        await bot.send_message(GROUP_ID, f"❌ سرور `{hostname}` ({ip}) از دسترس خارج شد.", parse_mode="Markdown")
    elif old == "غیرفعال" and new == "فعال":
        await bot.send_message(GROUP_ID, f"✅ سرور `{hostname}` ({ip}) دوباره در دسترس قرار گرفت.", parse_mode="Markdown")
