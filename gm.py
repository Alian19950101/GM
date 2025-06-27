from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ConversationHandler, ContextTypes, CallbackContext, JobQueue
)
import asyncio

OWNER_ID = 8101825425
BOT_TOKEN = "8181757436:AAEmcWIwZxdfv0JNG9t1jZ5LO6z2ob42IRc"

GET_SENTENCE, GET_ADVICE = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أرجو أن تكتب لي جملة مفيدة.")
    return GET_SENTENCE

async def get_sentence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['sentence'] = update.message.text
    await update.message.reply_text("شكراً! الآن أرسل لي نصيحة مفيدة.")
    return GET_ADVICE

async def get_advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['advice'] = update.message.text
    user = update.message.from_user
    sentence = context.user_data.get('sentence')
    advice = context.user_data.get('advice')

    message_to_owner = (
        f"📩 رسالة جديدة من @{user.username or user.first_name} (ID: {user.id}):\n\n"
        f"💡 جملة مفيدة:\n{sentence}\n\n"
        f"📝 نصيحة مفيدة:\n{advice}"
    )

    await context.bot.send_message(chat_id=OWNER_ID, text=message_to_owner)
    await update.message.reply_text("تم استلام جملتك ونصائحك وشكراً لك!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم إلغاء العملية. إذا أردت تبدأ من جديد، أرسل /start.")
    return ConversationHandler.END

async def send_periodic_message(context: CallbackContext):
    # هذه رسالة ترحيبية ترسلها لنفس البوت (صاحب البوت)
    await context.bot.send_message(chat_id=OWNER_ID, text="رسالة ترحيبية تلقائية كل 14 دقيقة. 👋")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GET_SENTENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sentence)],
            GET_ADVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_advice)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    # إضافة جدولة الرسائل الدورية كل 14 دقيقة
    job_queue = app.job_queue
    job_queue.run_repeating(send_periodic_message, interval=14*60, first=10)  # أول رسالة بعد 10 ثواني

    print("البوت شغال الآن...")
    app.run_polling()
