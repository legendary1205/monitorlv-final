# handlers/traffic.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import load_hosts, save_hosts, generate_id

pending_action = {}

async def handle_traffic_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    user_id = query.from_user.id
    if data.endswith("_add"):
        pending_action[user_id] = "add_traffic"
        await query.edit_message_text("🔧 لطفاً IP و هاست نیم را وارد کنید به صورت:\n`192.168.1.1 server1`", parse_mode="Markdown")
    elif data.endswith("_remove"):
        pending_action[user_id] = "remove_traffic"
        await query.edit_message_text("🗑 لطفاً IP و هاست نیم را برای حذف وارد کنید:")
    elif data.endswith("_list"):
        hosts = load_hosts()
        text = "📋 لیست سرورهای ترافیک:\n"
        for h in hosts:
            if h["type"] == "traffic":
                text += f"• `{h['ip']}` ({h['hostname']}) – {h['status']}\n"
        await query.edit_message_text(text or "هیچ آی‌پی ثبت نشده", parse_mode="Markdown")

async def handle_traffic_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    if pending_action[user_id] == "add_traffic":
        host_id = generate_id()
        hosts.append({"id": host_id, "ip": ip, "hostname": hostname, "type": "traffic", "status": "pending"})
        save_hosts(hosts)
        await update.message.reply_text(f"✅ سرور {hostname} ({ip}) اضافه شد.")

    elif pending_action[user_id] == "remove_traffic":
        hosts = [h for h in hosts if not (h["ip"] == ip and h["hostname"] == hostname and h["type"] == "traffic")]
        save_hosts(hosts)
        await update.message.reply_text(f"🗑 سرور {hostname} ({ip}) حذف شد.")

    del pending_action[user_id]
