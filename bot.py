# bot.py

import asyncio
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
)
from config import BOT_TOKEN
from handlers.panel import panel_handler, panel_callback
from handlers.ping import handle_ping_action, handle_ping_message
from handlers.traffic import handle_traffic_action, handle_traffic_message
from handlers.bandwidth import handle_bandwidth_action, handle_bandwidth_message

async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # فرمان اصلی پنل
    app.add_handler(CommandHandler("panel", panel_handler))
    
    # کلیک روی دکمه‌های پنل
    app.add_handler(CallbackQueryHandler(panel_callback))

    # کلیک روی دکمه‌های زیرمنو (افزودن/حذف/لیست)
    app.add_handler(CallbackQueryHandler(handle_ping_action, pattern="^ping_"))
    app.add_handler(CallbackQueryHandler(handle_traffic_action, pattern="^traffic_"))
    app.add_handler(CallbackQueryHandler(handle_bandwidth_action, pattern="^bandwidth_"))

    # پیام متنی برای افزودن/حذف آی‌پی
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ping_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_traffic_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_bandwidth_message))

    print("🤖 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
