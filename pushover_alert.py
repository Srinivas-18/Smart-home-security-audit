import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_pushover_notification(message, title="Smart Surveillance Alert"):
    token = os.getenv("PUSHOVER_API_TOKEN")
    user = os.getenv("PUSHOVER_USER_KEY")

    if not token or not user:
        print("Pushover API credentials are missing.")
        return

    payload = {
        "token": token,
        "user": user,
        "message": message,
        "title": title
    }

    try:
        response = requests.post("https://api.pushover.net/1/messages.json", data=payload)
        if response.status_code == 200:
            print("✅ Pushover alert sent successfully.")
        else:
            print("❌ Failed to send pushover alert:", response.text)
    except Exception as e:
        print("⚠️ Error sending pushover alert:", e)
