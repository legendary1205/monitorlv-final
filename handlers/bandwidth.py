# placeholder for bandwidth.py
# handlers/bandwidth.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import load_hosts, save_hosts, generate_id

user_state = {}

async def handle_bandwidth_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "bandwidth_add":
        user_state[query.from_user.id] = "adding_bandwidth"
        await query.edit_message_text("لطفاً IP و هاست‌نیم سرور پهنای باند را وارد کنید:\n`192.168.1.1 Hostname`", parse_mode="Markdown")
    elif data == "bandwidth_remove":
        user_state[query.from_user.id] = "removing_bandwidth"
        await query.edit_message_text("IP و هاست‌نیم سرور مورد نظر برای حذف را وارد کنید:")
    elif data == "bandwidth_list":
        hosts = load_hosts()
        bandwidth_hosts = [h for h in hosts if h["type"] == "bandwidth"]
        if not bandwidth_hosts:
            await query.edit_message_text("⛔️ هیچ سروری برای مانیتور پهنای باند ثبت نشده.")
        else:
            msg = "📋 لیست سرورهای مانیتور پهنای باند:\n\n"
            for h in bandwidth_hosts:
                msg += f"🔹 [{h['id']}] {h['hostname']} - {h['ip']}\n"
            await query.edit_message_text(msg)

async def handle_bandwidth_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = user_state.get(user_id)

    if state in ("adding_bandwidth", "removing_bandwidth"):
        try:
            ip, hostname = update.message.text.strip().split(maxsplit=1)
        except:
            await update.message.reply_text("❌ فرمت اشتباه است. لطفاً به صورت `IP Hostname` ارسال کنید.")
            return

        hosts = load_hosts()

        if state == "adding_bandwidth":
            host_id = generate_id()
            hosts.append({
                "id": host_id,
                "ip": ip,
                "hostname": hostname,
                "type": "bandwidth",
                "status": "pending"
            })
            save_hosts(hosts)
            await update.message.reply_text(f"✅ سرور پهنای باند با شناسه [{host_id}] اضافه شد.")

        elif state == "removing_bandwidth":
            original_len = len(hosts)
            hosts = [h for h in hosts if not (h["ip"] == ip and h["hostname"] == hostname and h["type"] == "bandwidth")]
            if len(hosts) < original_len:
                save_hosts(hosts)
                await update.message.reply_text("✅ سرور حذف شد.")
            else:
                await update.message.reply_text("❌ سرور مورد نظر یافت نشد.")

        user_state[user_id] = None
