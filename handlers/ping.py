# handlers/ping.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import load_hosts, save_hosts
import uuid

pending_action = {}

async def handle_ping_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    user_id = query.from_user.id
    if data.endswith("_add"):
        pending_action[user_id] = "add_ping"
        await query.edit_message_text("🔧 لطفاً IP و هاست نیم را وارد کنید به صورت:\n`192.168.1.1 server1`", parse_mode="Markdown")
    elif data.endswith("_remove"):
        pending_action[user_id] = "remove_ping"
        await query.edit_message_text("🗑 لطفاً IP و هاست نیم را برای حذف وارد کنید:")
    elif data.endswith("_list"):
        hosts = load_hosts()
        text = "📋 لیست سرورهای پینگ:\n"
        for h in hosts:
            if h["type"] == "ping":
                text += f"• `{h['ip']}` ({h['hostname']}) – {h['status']}\n"
        await query.edit_message_text(text or "هیچ آی‌پی ثبت نشده", parse_mode="Markdown")

async def handle_ping_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in pending_action:
        return

    text = update.message.text.strip()
    parts = text.split()

    if len(parts) != 2:
        await update.message.reply_text("❌ فرمت اشتباه است. لطفاً به صورت `IP Hostname` وارد کنید.")
        return

    ip, hostname = parts
    hosts = load_hosts()

    if pending_action[user_id] == "add_ping":
        host_id = str(uuid.uuid4())[:8]
        hosts.append({"id": host_id, "ip": ip, "hostname": hostname, "type": "ping", "status": "pending"})
        save_hosts(hosts)
        await update.message.reply_text(f"✅ سرور {hostname} ({ip}) اضافه شد.")

    elif pending_action[user_id] == "remove_ping":
        hosts = [h for h in hosts if not (h["ip"] == ip and h["hostname"] == hostname and h["type"] == "ping")]
        save_hosts(hosts)
        await update.message.reply_text(f"🗑 سرور {hostname} ({ip}) حذف شد.")

    del pending_action[user_id]
