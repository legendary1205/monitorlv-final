from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
)
from config import BOT_TOKEN
from handlers.panel import panel_handler, panel_callback
from handlers.ping import handle_ping_action
from handlers.traffic import handle_traffic_action
from handlers.bandwidth import handle_bandwidth_action
from handlers.shared_message_handler import handle_shared_message

async def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()

    # فرمان باز کردن پنل
    app.add_handler(CommandHandler("panel", panel_handler))

    # دکمه‌های پنل اصلی و بازگشت
    app.add_handler(CallbackQueryHandler(panel_callback, pattern="^monitor_|^panel$"))

    # هندل کردن دکمه‌های هر مانیتور
    app.add_handler(CallbackQueryHandler(handle_ping_action, pattern="^ping_"))
    app.add_handler(CallbackQueryHandler(handle_traffic_action, pattern="^traffic_"))
    app.add_handler(CallbackQueryHandler(handle_bandwidth_action, pattern="^bandwidth_"))

    # پیام‌های متنی برای افزودن/حذف IP
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_shared_message))

    print("🤖 Bot is running...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
