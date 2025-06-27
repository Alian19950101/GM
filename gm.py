import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ConversationHandler, ContextTypes
)

OWNER_ID = 8101825425
BOT_TOKEN = "8181757436:AAEmcWIwZxdfv0JNG9t1jZ5LO6z2ob42IRc"

GET_SENTENCE, GET_ADVICE = range(2)

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أرجو أن تكتب لي جملة مفيدة.")
    return GET_SENTENCE

async def get_sentence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['sentence'] = update.message.text
    await update.message.reply_text("شكراً! الآن أرسل لي نصيحة مفيدة.")
    return GET_ADVICE

async def get_advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sentence = context.user_data['sentence']
    advice = update.message.text
    user = update.message.from_user

    msg = (
        f"📩 رسالة من @{user.username or user.first_name} (ID: {user.id}):\n\n"
        f"💡 جملة مفيدة:\n{sentence}\n\n"
        f"📝 نصيحة مفيدة:\n{advice}"
    )
    await context.bot.send_message(chat_id=OWNER_ID, text=msg)
    await update.message.reply_text("تم الإرسال! شكرًا لك 😄")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم الإلغاء. أرسل /start عند الاستعداد.")
    return ConversationHandler.END

async def periodic_welcome(app):
    await asyncio.sleep(10)  # البداية بعد 10 ثواني
    while True:
        await app.bot.send_message(chat_id=OWNER_ID, text="👋 ترحيب تلقائي كل 14 دقيقة")
        await asyncio.sleep(14 * 60)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start_cmd)],
        states={
            GET_SENTENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sentence)],
            GET_ADVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_advice)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv)

    # بدء مهمة الرسائل الدورية
    app.after_startup.add_callback(lambda _: asyncio.create_task(periodic_welcome(app)))

    print("🚀 البوت يعمل الآن!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
