# placeholder for traffic.py
# handlers/traffic.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import load_hosts, save_hosts, generate_id

user_state = {}

async def handle_traffic_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "traffic_add":
        user_state[query.from_user.id] = "adding_traffic"
        await query.edit_message_text("لطفاً IP و هاست‌نیم سرور ترافیک را وارد کنید:\n`192.168.1.1 Hostname`", parse_mode="Markdown")
    elif data == "traffic_remove":
        user_state[query.from_user.id] = "removing_traffic"
        await query.edit_message_text("IP و هاست‌نیم سرور مورد نظر برای حذف را وارد کنید:")
    elif data == "traffic_list":
        hosts = load_hosts()
        traffic_hosts = [h for h in hosts if h["type"] == "traffic"]
        if not traffic_hosts:
            await query.edit_message_text("⛔️ هیچ سروری برای مانیتور ترافیک ثبت نشده.")
        else:
            msg = "📋 لیست سرورهای مانیتور ترافیک:\n\n"
            for h in traffic_hosts:
                msg += f"🔹 [{h['id']}] {h['hostname']} - {h['ip']}\n"
            await query.edit_message_text(msg)

async def handle_traffic_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = user_state.get(user_id)

    if state in ("adding_traffic", "removing_traffic"):
        try:
            ip, hostname = update.message.text.strip().split(maxsplit=1)
        except:
            await update.message.reply_text("❌ فرمت اشتباه است. لطفاً به صورت `IP Hostname` ارسال کنید.")
            return

        hosts = load_hosts()

        if state == "adding_traffic":
            host_id = generate_id()
            hosts.append({
                "id": host_id,
                "ip": ip,
                "hostname": hostname,
                "type": "traffic",
                "status": "pending"
            })
            save_hosts(hosts)
            await update.message.reply_text(f"✅ سرور ترافیک با شناسه [{host_id}] اضافه شد.")

        elif state == "removing_traffic":
            original_len = len(hosts)
            hosts = [h for h in hosts if not (h["ip"] == ip and h["hostname"] == hostname and h["type"] == "traffic")]
            if len(hosts) < original_len:
                save_hosts(hosts)
                await update.message.reply_text("✅ سرور حذف شد.")
            else:
                await update.message.reply_text("❌ سرور مورد نظر یافت نشد.")

        user_state[user_id] = None
