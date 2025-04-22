# placeholder for ping.py
# handlers/ping.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import load_hosts, save_hosts, generate_id

user_state = {}

async def handle_ping_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "ping_add":
        user_state[query.from_user.id] = "adding_ping"
        await query.edit_message_text("لطفاً IP و هاست‌نیم سرور پینگ را وارد کنید:\n`192.168.1.1 Hostname`", parse_mode="Markdown")
    elif data == "ping_remove":
        user_state[query.from_user.id] = "removing_ping"
        await query.edit_message_text("IP و هاست‌نیم سرور مورد نظر برای حذف را وارد کنید:")
    elif data == "ping_list":
        hosts = load_hosts()
        ping_hosts = [h for h in hosts if h["type"] == "ping"]
        if not ping_hosts:
            await query.edit_message_text("⛔️ هیچ سروری برای مانیتور پینگ ثبت نشده.")
        else:
            msg = "📋 لیست سرورهای مانیتور پینگ:\n\n"
            for h in ping_hosts:
                msg += f"🔹 [{h['id']}] {h['hostname']} - {h['ip']}\n"
            await query.edit_message_text(msg)

async def handle_ping_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = user_state.get(user_id)

    if state in ("adding_ping", "removing_ping"):
        try:
            ip, hostname = update.message.text.strip().split(maxsplit=1)
        except:
            await update.message.reply_text("❌ فرمت اشتباه است. لطفاً به صورت `IP Hostname` ارسال کنید.")
            return

        hosts = load_hosts()

        if state == "adding_ping":
            host_id = generate_id()
            hosts.append({
                "id": host_id,
                "ip": ip,
                "hostname": hostname,
                "type": "ping",
                "status": "pending"
            })
            save_hosts(hosts)
            await update.message.reply_text(f"✅ سرور پینگ با شناسه [{host_id}] اضافه شد.")

        elif state == "removing_ping":
            original_len = len(hosts)
            hosts = [h for h in hosts if not (h["ip"] == ip and h["hostname"] == hostname and h["type"] == "ping")]
            if len(hosts) < original_len:
                save_hosts(hosts)
                await update.message.reply_text("✅ سرور حذف شد.")
            else:
                await update.message.reply_text("❌ سرور مورد نظر یافت نشد.")

        user_state[user_id] = None
