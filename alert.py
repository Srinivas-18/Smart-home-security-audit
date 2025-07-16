# alert.py

from pushover_alert import send_pushover_notification
from sms_alert import send_sms_alert

def send_all_alerts(message):
    print("📢 Sending alerts...")
    send_pushover_notification(message)
    send_sms_alert(message)
