# monitor_loop.py

import asyncio
import time
from telegram import Bot
from config import BOT_TOKEN, GROUP_ID
from utils.pingcheck import is_online
from utils.snmp import get_bandwidth_usage
from utils.storage import load_hosts, save_hosts

bot = Bot(BOT_TOKEN)
last_change = {}  # شناسه سرور → timestamp آخرین وضعیت

async def monitor_loop():
    while True:
        hosts = load_hosts()
        changed = False

        for host in hosts:
            host_id = host["id"]
            status_before = host.get("status", "pending")
            current_status = status_before

            if host["type"] == "ping":
                current_status = "active" if is_online(host["ip"]) else "down"

            elif host["type"] == "bandwidth":
                current_status = "active" if get_bandwidth_usage(host["ip"]) else "down"

            elif host["type"] == "traffic":
                current_status = "active" if is_online(host["ip"]) else "down"

            if current_status != status_before:
                now = time.time()
                changed = True
                host["status"] = current_status

                # اگر از active به down رفت
                if status_before == "active" and current_status == "down":
                    last_change[host_id] = now
                    await bot.send_message(
                        chat_id=GROUP_ID,
                        text=f"🚨 سرور {host['hostname']} ({host['ip']}) قطع شد."
                    )

                # اگر از down به active برگشت
                elif status_before == "down" and current_status == "active":
                    prev_time = last_change.get(host_id, now)
                    downtime = round((now - prev_time) / 60, 1)
                    await bot.send_message(
                        chat_id=GROUP_ID,
                        text=f"✅ سرور {host['hostname']} ({host['ip']}) وصل شد. \n⏱ مدت قطعی: {downtime} دقیقه"
                    )

        if changed:
            save_hosts(hosts)
            print(f"[{time.ctime()}] وضعیت سرورها ذخیره شد.")
        else:
            print(f"[{time.ctime()}] بدون تغییر در وضعیت.")

        await asyncio.sleep(30)
