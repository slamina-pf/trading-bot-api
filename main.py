import threading
from app.app_test import app
from bot.bot_test import run_bot

def start_bots():

    threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    start_bots()
    app.run(host="0.0.0.0", port=5000)