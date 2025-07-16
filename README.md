# 🔐 Smart Surveillance System 2.0
> Next-Gen Motion & Face Recognition with Real-Time Alerts, Logs & GUI

![Banner](https://raw.githubusercontent.com/Srinivas-18/Smart-home-security-audit/main/github-header-image.png)

<div align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" />
  <img src="https://img.shields.io/badge/OpenCV-RealTime-green" />
  <img src="https://img.shields.io/badge/Security-Log%20Protected-critical" />
  <img src="https://img.shields.io/badge/Alerts-SMS%2FPush-blueviolet" />
</div>

---

## 🚀 Features

✅ Real-time motion & theft detection  
✅ Face recognition with training UI  
✅ Email, SMS, and push notifications  
✅ Snapshots saved automatically  
✅ CSV logging with secure access  
✅ Beautiful & intuitive Tkinter GUI  

---

## 🖥️ Interface Overview

| Feature        | Description                             |
|----------------|-----------------------------------------|
| 🕵️ Monitor      | Detects motion & sends alerts instantly |
| 😎 Identify     | Trains and detects known faces          |
| 🟩 Rectangle    | Visual motion overlay test              |
| 📹 Record       | Records video with timestamp            |
| 🔄 In/Out       | Detects directional movement            |
| 📋 View Log     | Opens secure alert log (password-protected) |
| 🚪 Exit         | Exits GUI safely                        |

---

## 🧪 Tech Stack
- **Python 3.10+**
- **OpenCV** for video and face detection
- **Pillow (PIL)** for GUI images (optional)
- **dotenv** for config management
- **Twilio & Pushover** for alerts
- **Tkinter** for GUI frontend

---

## 📁 Project Structure
```bash
📦 SmartSurveillance/
├── main.py               # Main GUI interface
├── find_motion.py        # Motion detection + alert
├── identify.py           # Face recognition logic
├── record.py             # Recording video
├── in_out.py             # Direction detection
├── alert.py              # Sends email/SMS/push alerts
├── alert_log.csv         # Auto-generated alert logs
├── persons/              # Trained face images
├── stolen/               # Motion snapshots
├── .env                  # Environment variables (not uploaded)
├── .env.example          # 🔐 Template for user credentials
└── README.md
```

> 📦 NOTE: If you want the button icons to work properly, you need to create a folder named `icons/` and place appropriate images inside it. Refer to filenames used in `main.py` (e.g., `mon1.png`, `rec1.png`, etc.)

---

## 🔐 .env Setup

Create a `.env` file from `.env.example`:

```env
# Email Alerts
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_password_or_appkey
TO_EMAIL=receiver@example.com

# Twilio SMS
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890
USER_PHONE_NUMBER=+91xxxxxxxxxx

# Pushover Notifications
PUSHOVER_USER_KEY=your_pushover_user_key
PUSHOVER_API_KEY=your_pushover_api_key

# GUI Log Security
LOG_USERNAME=admin
LOG_PASSWORD=1234
```

📌 **Never commit your `.env` file!** Use `.env.example` for sharing.

---

## ⚙️ Installation & Running

### 🔧 Install dependencies
```bash
pip install -r requirements.txt
```
_Or manually:_
```bash
pip install opencv-python pillow python-dotenv twilio requests
```

### ▶️ Run the App
```bash
python main.py
```

---

## 🛡️ Secure Features
- 🔑 Log access only with username/password
- 🚨 Alerts only on real motion (not noise)
- 💾 All images saved with timestamp

---

## 💡 Future Enhancements
- 🔁 Cloud image sync (Google Drive/Firebase)
- 📱 Telegram/WhatsApp alert integration
- 📊 Web dashboard (Streamlit/Flask)
- 🔍 Object detection (weapons, bags, etc.)
- 👥 Multi-user login + role-based access

---

## 🙌 Author
**VARIGONDA LAKSHMI SRINIVAS**  
[GitHub → Srinivas-18](https://github.com/Srinivas-18)

---

## 📄 License
MIT License — not free to use and modify, give credit!

---

> ⭐ Star this repo if you like it. Fork if you want to build on it. PRs welcome!
