# handlers/shared_message_handler.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import load_hosts, save_hosts, generate_id
from handlers.ping import pending_action as ping_pending
from handlers.traffic import pending_action as traffic_pending
from handlers.bandwidth import pending_action as bandwidth_pending

async def handle_shared_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    parts = text.split()

    if len(parts) != 2:
        await update.message.reply_text("❌ فرمت اشتباه است. لطفاً به صورت `IP Hostname` وارد کنید.")
        return

    ip, hostname = parts
    hosts = load_hosts()

    if user_id in ping_pending:
        action = ping_pending.pop(user_id)
        htype = "ping"
    elif user_id in traffic_pending:
        action = traffic_pending.pop(user_id)
        htype = "traffic"
    elif user_id in bandwidth_pending:
        action = bandwidth_pending.pop(user_id)
        htype = "bandwidth"
    else:
        return  # کاربر در حالت خاصی نیست

    if action.startswith("add_"):
        host_id = generate_id()
        hosts.append({"id": host_id, "ip": ip, "hostname": hostname, "type": htype, "status": "pending"})
        save_hosts(hosts)
        await update.message.reply_text(f"✅ سرور {hostname} ({ip}) اضافه شد.")
    elif action.startswith("remove_"):
        hosts = [h for h in hosts if not (h["ip"] == ip and h["hostname"] == hostname and h["type"] == htype)]
        save_hosts(hosts)
        await update.message.reply_text(f"🗑 سرور {hostname} ({ip}) حذف شد.")
