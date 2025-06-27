import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters, ConversationHandler
)

# 🆔 معرفك الشخصي في تيليجرام
OWNER_ID = 8101825425
# 🔑 توكن البوت الخاص بك
BOT_TOKEN = "8181757436:AAEmcWIwZxdfv0JNG9t1jZ5LO6z2ob42IRc"

# مراحل المحادثة
GET_SENTENCE, GET_ADVICE = range(2)

# بدء المحادثة
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 مرحبًا! أرسل لي جملة مفيدة.")
    return GET_SENTENCE

# استقبال الجملة المفيدة
async def receive_sentence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["sentence"] = update.message.text
    await update.message.reply_text("✅ جيد! الآن أرسل لي نصيحة مفيدة.")
    return GET_ADVICE

# استقبال النصيحة المفيدة
async def receive_advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    advice = update.message.text
    sentence = context.user_data.get("sentence", "لم يتم إدخال جملة.")

    user = update.message.from_user
    message = (
        f"📥 رسالة من @{user.username or user.first_name} (ID: {user.id})\n\n"
        f"📌 الجملة المفيدة:\n{sentence}\n\n"
        f"💡 النصيحة المفيدة:\n{advice}"
    )
    await context.bot.send_message(chat_id=OWNER_ID, text=message)
    await update.message.reply_text("✅ شكراً لك! تم إرسال الرسالة.")

    return ConversationHandler.END

# إلغاء المحادثة
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ تم الإلغاء.")
    return ConversationHandler.END

# رسالة ترحيبية كل 14 دقيقة
async def send_periodic_welcome(bot):
    await asyncio.sleep(10)
    while True:
        await bot.send_message(chat_id=OWNER_ID, text="👋 أهلاً بك! (رسالة ترحيب دورية)")
        await asyncio.sleep(14 * 60)

# تشغيل البوت
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GET_SENTENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_sentence)],
            GET_ADVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_advice)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    # بدء مهمة الترحيب الدورية
    app.post_init(lambda _: asyncio.create_task(send_periodic_welcome(app.bot)))

    print("✅ البوت يعمل الآن...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
