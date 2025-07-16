import cv2
import time
import os
from datetime import datetime
from alert import send_all_alerts
import csv

os.makedirs("stolen", exist_ok=True)
log_file = "alert_log.csv"

if not os.path.exists(log_file):
    with open(log_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Image", "Alert Message"])

def find_motion():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Failed to open camera.")
        return

    countdown_start = time.time()
    countdown_duration = 5

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        elapsed = time.time() - countdown_start
        remaining = int(countdown_duration - elapsed)

        if remaining > 0:
            display = frame.copy()
            cv2.putText(display, f"Starting in {remaining}s", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow("Live Feed - ESC to exit", display)
            if cv2.waitKey(1) == 27:
                cap.release()
                cv2.destroyAllWindows()
                return
        else:
            break

    _, frm1 = cap.read()
    frm1_gray = cv2.cvtColor(frm1, cv2.COLOR_BGR2GRAY)
    last_alert_time = 0

    while True:
        ret, frm2 = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frm2, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(frm1_gray, gray)
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        contours = [c for c in contours if cv2.contourArea(c) > 100]

        display_frame = frm2.copy()

        if len(contours) > 5:
            cv2.putText(display_frame, "🚨 Motion Detected!", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if time.time() - last_alert_time > 5:
                timestamp = datetime.now().strftime('%d-%m-%y %H:%M:%S')
                filename = f"stolen/{datetime.now().strftime('%d-%m-%y-%H-%M-%S')}.jpg"
                cv2.imwrite(filename, frm2)

                alert_msg = "🚨 Motion detected in surveillance area!"
                send_all_alerts(alert_msg)
                print("✅ Alert sent! Snapshot saved:", filename)

                with open(log_file, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, filename, alert_msg])

                last_alert_time = time.time()
        else:
            cv2.putText(display_frame, "No Motion", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        frm1_gray = gray
        cv2.imshow("Live Feed - ESC to exit", display_frame)

        if cv2.waitKey(1) == 27:
            cap.release()
            cv2.destroyAllWindows()
            break
