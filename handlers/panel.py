# handlers/panel.py

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from config import ADMIN_ID

async def panel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔️ دسترسی ندارید.")
        return

    keyboard = [
        [InlineKeyboardButton("📶 مانیتور پینگ", callback_data="monitor_ping")],
        [InlineKeyboardButton("📊 مانیتور ترافیک", callback_data="monitor_traffic")],
        [InlineKeyboardButton("📡 مانیتور پهنای باند", callback_data="monitor_bandwidth")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎛 لطفاً مانیتور مورد نظر را انتخاب کنید:", reply_markup=reply_markup)

async def panel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("monitor_"):
        kind = data.split("_")[1]
        await send_subpanel(query, kind)
    elif data == "panel":
        await panel_handler(update, context)

async def send_subpanel(query, kind):
    title_map = {"ping": "پینگ", "traffic": "ترافیک", "bandwidth": "پهنای باند"}
    keyboard = [
        [InlineKeyboardButton("➕ افزودن", callback_data=f"{kind}_add")],
        [InlineKeyboardButton("❌ حذف", callback_data=f"{kind}_remove")],
        [InlineKeyboardButton("📋 لیست", callback_data=f"{kind}_list")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="panel")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"🎛 عملیات برای مانیتور {title_map.get(kind, kind)}:", reply_markup=reply_markup)

