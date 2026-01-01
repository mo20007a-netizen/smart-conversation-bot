import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openai import OpenAI

# =========================
# بياناتك (عدّل هنا فقط)
# =========================
TELEGRAM_TOKEN = "8586327251:AAERirHuv2kZ-wTA8bH8B4VnK2zgJZh8I_U"
OPENAI_API_KEY = "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"
DEVELOPER_NAME = "Mostafa Nour"

# =========================
# إعداد OpenAI
# =========================
client = OpenAI(api_key=OPENAI_API_KEY)

# =========================
# إعداد اللوج
# =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# =========================
# رسالة البداية
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 أهلاً بيك!\n\n"
        "ابعت أي رسالة وأنا هرد عليك باستخدام الذكاء الاصطناعي 🤖✨\n\n"
        f"🔹 تطوير: {DEVELOPER_NAME}"
    )
    await update.message.reply_text(welcome_text)

# =========================
# الرد على الرسائل
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "أنت مساعد ذكي تتحدث باللغة العربية وتساعد المستخدمين بشكل واضح وبسيط.",
                },
                {"role": "user", "content": user_text},
            ],
        )

        ai_reply = response.choices[0].message.content

    except Exception:
        ai_reply = "⚠️ حصل خطأ مؤقت في الذكاء الاصطناعي، حاول تاني بعد شوية."

    final_reply = f"{ai_reply}\n\n— تطوير: {DEVELOPER_NAME}"
    await update.message.reply_text(final_reply)

# =========================
# تشغيل البوت
# =========================
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
