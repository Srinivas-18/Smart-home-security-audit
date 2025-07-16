# sms_alert.py

import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_sms_alert(body):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_PHONE_NUMBER")
    to_number = os.getenv("TARGET_PHONE_NUMBER")

    if not account_sid or not auth_token or not from_number or not to_number:
        print("❌ Twilio credentials are missing.")
        return

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=to_number
        )
        print("✅ SMS sent successfully:", message.sid)
    except Exception as e:
        print("⚠️ Failed to send SMS:", e)
