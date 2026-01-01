import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# ====== إعدادات ======
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEVELOPER_NAME = "Mostafa Nour"

client = OpenAI(api_key=OPENAI_API_KEY)

# ====== /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 أهلاً بيك!\n"
        "ابعت أي رسالة وأنا هرد عليك بالذكاء الاصطناعي ✨\n\n"
        f"— تطوير: {DEVELOPER_NAME}"
    )

# ====== الرسائل ======
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي عربي، ترد بشكل واضح ومفيد."},
                {"role": "user", "content": user_text}
            ]
        )
        reply = response.choices[0].message.content
    except Exception:
        reply = "⚠️ حصل خطأ مؤقت، حاول تاني بعد شوية."

    await update.message.reply_text(
        f"{reply}\n\n— تطوير: {DEVELOPER_NAME}"
    )

# ====== تشغيل ======
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
