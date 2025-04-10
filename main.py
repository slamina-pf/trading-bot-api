import threading
from app.app_test import app

def start_bots():
    return "Starting bots..."
    #threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    start_bots()
    app.run(host="0.0.0.0", port=5000)