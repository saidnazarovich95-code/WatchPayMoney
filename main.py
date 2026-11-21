

import os
import json
import urllib.request
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")
APP_URL = "https://saidnazarovich95-code.github.io/WatchPayMoney/"
SERVER_URL = "https://watchpaymoney.onrender.com"

def telegram(method, data):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read())

def setup_webhook():
    if not BOT_TOKEN or not WEBHOOK_SECRET:
        print("Missing environment variables!")
        return

    try:
        result = telegram("setWebhook", {
            "url": SERVER_URL + "/webhook",
            "secret_token": WEBHOOK_SECRET,
            "allowed_updates": ["message"]
        })
        print("Webhook setup:", result)
    except Exception as e:
        print("Webhook error:", e)

@app.route("/")
def home():
    return "WatchPayMoney server is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token"
    ) != WEBHOOK_SECRET:
        return "Unauthorized", 403

    update = request.get_json(silent=True) or {}
    message = update.get("message", {})
    chat = message.get("chat", {})
    text = message.get("text", "")

    if not chat:
        return "OK"

    chat_id = chat["id"]

    if text == "/start":
        telegram("sendMessage", {
            "chat_id": chat_id,
            "text": "Welcome to WatchPayMoney! 🎉",
            "reply_markup": {
                "inline_keyboard": [[{
                    "text": "🚀 Open App",
                    "web_app": {"url": APP_URL}
                }]]
            }
        })

    elif text == "/balance":
        telegram("sendMessage", {
            "chat_id": chat_id,
            "text": "Your balance: $0.00 USDT (Demo)"
        })

    else:
        telegram("sendMessage", {
            "chat_id": chat_id,
            "text": "Welcome! Use /start to open WatchPayMoney."
        })

    return "OK"

if __name__ == "__main__":
    setup_webhook()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
