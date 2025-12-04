# 🔐 Smart Surveillance System 2.0
> Next-Gen Motion & Face Recognition with Real-Time Alerts, Logs & GUI

![Banner](https://raw.githubusercontent.com/Srinivas-18/Smart-home-security-audit/main/github-header-image.png)
![Banner](https://raw.githubusercontent.com/pranay-04/Smart-home-security-audit/main/github-header-image.png)

<div align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" />
  <img src="https://img.shields.io/badge/OpenCV-RealTime-green" />
  <img src="https://img.shields.io/badge/Security-Log%20Protected-critical" />
  <img src="https://img.shields.io/badge/Alerts-SMS%2FPush-blueviolet" />
</div>

---

## 📋 Table of Contents
- [Features](#-features)
- [Project Overview](#-project-overview)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Detailed Modules](#-detailed-modules)
- [Project Structure](#-project-structure)
- [Interface Overview](#-interface-overview)
- [Installation & Setup](#-installation--setup)
- [Environment Configuration](#-environment-configuration)
- [Usage Guide](#-usage-guide)
- [Security Features](#-security-features)
- [Future Enhancements](#-future-enhancements)
- [Authors](#-authors)
- [License](#-license)

---

## 🚀 Features

✅ **Real-time Motion Detection** - Advanced motion detection with background subtraction and contour analysis  
✅ **Face Recognition System** - LBPH-based face recognition with training UI and database management  
✅ **Multi-Channel Alerts** - Email, SMS (Twilio), and Push notifications (Pushover)  
✅ **Automatic Snapshots** - Timestamped images saved for motion events and intrusions  
✅ **Professional Logging** - Excel-based structured logging with categorized event tracking  
✅ **Interactive GUI** - Beautiful Tkinter-based interface with icon buttons and real-time feedback  
✅ **Entry/Exit Tracking** - Directional movement detection for visitor monitoring  
✅ **Video Recording** - Timestamped video recording with codec optimization  
✅ **Rectangle Motion Detection** - Custom region-of-interest (ROI) motion monitoring  
✅ **Password-Protected Logs** - Secure access to surveillance logs with authentication  

---

## 🔍 Project Overview

The **Smart Surveillance System 2.0** is a comprehensive Python-based security solution designed for home and office monitoring. It combines computer vision techniques (OpenCV), machine learning (face recognition), and real-time alerting to create a robust security infrastructure.

### Key Capabilities:
- **Intelligent Motion Detection**: Uses frame differencing and contour analysis to detect actual movement, filtering out noise
- **Face Recognition**: Train the system with known faces and get real-time identification with confidence scores
- **Multi-tier Alerting**: Instant notifications via Email, SMS, and Push notifications when threats are detected
- **Comprehensive Logging**: All events logged in structured Excel format with timestamps and categorization
- **User-Friendly Interface**: No command-line expertise required - everything accessible through GUI buttons

### Use Cases:
- Home security monitoring
- Office entrance surveillance
- Theft detection and prevention
- Visitor tracking and logging
- Remote monitoring with instant alerts

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE (GUI)                     │
│                      main.py (Tkinter)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┬─────────────┐
         │             │             │             │
    ┌────▼───┐   ┌────▼────┐   ┌───▼────┐   ┌────▼────┐
    │ Motion │   │  Face   │   │ Entry/ │   │ Video   │
    │Detection│   │ Recog.  │   │  Exit  │   │Recording│
    └────┬───┘   └────┬────┘   └───┬────┘   └────┬────┘
         │            │            │             │
         └────────────┼────────────┼─────────────┘
                      │            │
              ┌───────▼────────────▼───────┐
              │   ALERT SYSTEM (alert.py)  │
              │  ├─ Email (SMTP)           │
              │  ├─ SMS (Twilio)           │
              │  └─ Push (Pushover)        │
              └───────┬────────────────────┘
                      │
              ┌───────▼────────────────────┐
              │  LOGGING SYSTEM            │
              │  ├─ Excel Logs (logger.py) │
              │  ├─ CSV Logs (legacy)      │
              │  └─ Log Viewer (GUI)       │
              └────────────────────────────┘
```

---

## 🧪 Tech Stack

### Core Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.10+ | Primary programming language |
| **OpenCV** | Latest | Computer vision, camera access, image processing |
| **Tkinter** | Built-in | GUI framework for user interface |
| **Pillow (PIL)** | Latest | Image manipulation for GUI icons |
| **NumPy** | Latest | Array operations for image processing |

### Face Recognition
| Library | Purpose |
|---------|---------|
| **cv2.face.LBPHFaceRecognizer** | Local Binary Patterns Histograms for face recognition |
| **Haar Cascade Classifier** | Face detection in video frames |

### Alert Systems
| Service | Library | Purpose |
|---------|---------|---------|
| **Email** | smtplib | SMTP-based email alerts |
| **Twilio** | twilio | SMS notifications via Twilio API |
| **Pushover** | requests | Push notifications to mobile devices |

### Logging & Data Management
| Library | Purpose |
|---------|---------|
| **Pandas** | DataFrame operations for log management |
| **OpenPyXL** | Excel file creation and manipulation |
| **JSON** | Person database storage |
| **CSV** | Legacy log file format |

### Configuration
| Tool | Purpose |
|------|---------|
| **python-dotenv** | Environment variable management (.env files) |

---

## 📦 Detailed Modules

### 1. **main.py** - Main GUI Application
The central hub of the application that provides a user-friendly interface.

**Features:**
- Professional Tkinter GUI with custom icons
- 7 main function buttons (Monitor, Identify, Rectangle, Record, In/Out, View Log, Exit)
- System event logging for all user actions
- Automatic log viewer integration

**Key Functions:**
```python
- monitor_with_logging()    # Launch motion detection
- identify_with_logging()   # Launch face recognition
- rectangle_with_logging()  # Custom ROI motion detection
- record_with_logging()     # Video recording
- in_out_with_logging()     # Entry/exit tracking
- open_log()                # Professional log viewer
```

---

### 2. **find_motion.py** - Advanced Motion Detection
Implements lag-free motion detection with intelligent filtering.

**Technical Details:**
- **Algorithm**: Background subtraction with Gaussian blur
- **Frame Processing**: 640x480 @ 30 FPS with MJPEG codec
- **Buffer Optimization**: 1-frame buffer to minimize lag
- **Motion Threshold**: 3000 pixels (configurable)
- **Alert Cooldown**: 5 seconds between alerts

**Features:**
- Real-time motion area calculation
- Contour-based motion detection
- Automatic image capture on motion
- Background worker thread for non-blocking alerts
- Dynamic reference frame updates

**Output:**
- Saves snapshots to `stolen/` directory
- Logs to CSV and Excel
- Triggers multi-channel alerts

---

### 3. **identify.py** - Face Recognition System
Complete face recognition implementation with training and recognition modes.

**Architecture:**
```
FaceRecognitionSystem
├── Person Database (JSON)
├── Training Images (persons/)
├── LBPH Model (enhanced_model.yml)
└── GUI Components (Add/Manage/Recognize)
```

**Key Features:**
- **Training Phase**: Collects 100 high-quality face samples per person
- **Preprocessing**: Histogram equalization + Gaussian blur
- **Recognition**: LBPH algorithm with confidence threshold <80
- **Database**: JSON-based person registry with metadata

**GUI Functions:**
1. **Add New Person**: Interactive face capture with progress bar
2. **View/Manage Persons**: Tree view of registered faces with delete capability
3. **Start Recognition**: Real-time face identification with confidence display

**Technical Specifications:**
- Face size normalization: 200x200 pixels
- Detection: Haar Cascade with scale factor 1.1
- Min neighbors: 5 (reduces false positives)
- Confidence display: Color-coded (Green <80, Red ≥80)

---

### 4. **record.py** - Video Recording Module
Records timestamped video with real-time overlay.

**Specifications:**
- **Codec**: XVID (cross-platform compatibility)
- **Resolution**: 640x480
- **Frame Rate**: 20 FPS
- **Output Format**: .avi files

**Features:**
- Real-time timestamp overlay on video
- Automatic duration calculation
- Saves to `recordings/` directory
- Logs start/stop events with duration

---

### 5. **in_out.py** - Entry/Exit Detection
Tracks directional movement across detection zones.

**Detection Zones:**
- **Left Boundary**: x=200 (Entry zone)
- **Right Boundary**: x=500 (Exit zone)
- **Trigger**: Object crossing from one zone to another

**Logic:**
1. Object enters from right (x>500) → tracks as "potential exit"
2. Object crosses to left (x<200) → logs as "Entry"
3. Object enters from left (x<200) → tracks as "potential entry"
4. Object crosses to right (x>500) → logs as "Exit"

**Output:**
- Entry images: `visitors/in/`
- Exit images: `visitors/out/`
- Directional logging with timestamps

---

### 6. **alert.py** - Unified Alert Dispatcher
Central alert management system.

**Structure:**
```python
send_all_alerts(message)
    ├── send_pushover_notification(message)
    ├── send_sms_alert(message)
    └── (Email alerts can be added)
```

**Alert Flow:**
1. Motion detected → `find_motion.py` triggers alert
2. `alert.py` dispatches to all channels simultaneously
3. Each service sends notification independently
4. Failures logged but don't block other channels

---

### 7. **pushover_alert.py** - Push Notifications
Sends push notifications via Pushover API.

**Configuration:**
- Requires: `PUSHOVER_USER_KEY`, `PUSHOVER_API_KEY`
- Endpoint: `https://api.pushover.net/1/messages.json`
- Priority: Normal (can be configured to high priority)

---

### 8. **sms_alert.py** - SMS Notifications
Sends SMS via Twilio API.

**Configuration:**
- Requires: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`, `USER_PHONE_NUMBER`
- Uses Twilio REST API
- Supports international numbers

---

### 9. **logger.py** - Professional Logging System
Excel-based structured logging with categorization.

**Log Categories (Separate Sheets):**
1. **Motion Detection**: Status, area, alerts, images, duration
2. **Face Recognition**: Actions, person details, confidence scores
3. **Entry/Exit**: Direction, person count, location
4. **Recording**: File paths, duration, resolution
5. **Rectangle Motion**: Custom ROI monitoring events
6. **System Events**: Application lifecycle events

**Features:**
- Auto-initialized Excel workbook with formatted headers
- Color-coded rows (errors=red, success=green, warnings=yellow)
- Alternating row colors for readability
- Automatic column width adjustment
- Thread-safe writing

**File Location**: `logs/surveillance_logs.xlsx`

---

### 10. **log_viewer.py** - Professional Log Viewer GUI
Interactive log viewing interface with filtering and export capabilities.

**Features:**
- Tabbed interface for each log category
- Date range filtering (Today, Yesterday, 7 days, 30 days, All)
- Search functionality
- Export to Excel/CSV
- Right-click context menu (Copy, Open Image, Delete)
- Real-time statistics dashboard
- Sortable columns

**UI Components:**
- Header with summary statistics
- Notebook with 6 tabs (one per log category)
- Control panel with Refresh, Export, Clear, Statistics buttons
- Filter dropdown for date ranges
- Context menu for row operations

---

### 11. **rect_noise.py** - Rectangle Motion Detection
Custom region-of-interest (ROI) motion monitoring.

**Workflow:**
1. **Selection Phase**: Click and drag to select monitoring region
2. **Confirmation**: Press SPACE to confirm selection
3. **Monitoring Phase**: Continuous motion detection within selected area

**Features:**
- Interactive ROI selection with visual feedback
- Real-time motion area calculation
- Contour visualization within ROI
- Semi-transparent overlay on motion
- Adjustable sensitivity threshold (default: 1000)

---

### 12. **motion.py** - Basic Motion Detection
Simplified motion detection for testing purposes.

**Differences from find_motion.py:**
- No alerting system
- No image capture
- Simpler visualization
- Used for development/testing

---

### 13. **spot_diff.py, just_for_test.py, test_push.py, test_sms.py**
Testing and development utilities for validating individual components.

---

## 📁 Project Structure

```bash
📦 Smart-home-security-audit-FINAL/
│
├── 🎨 GUI & Main Application
│   ├── main.py                      # Main GUI application (Tkinter)
│   └── icons/                       # GUI button icons
│       ├── mon1.png                 # Monitor button icon
│       ├── rec1.png                 # Record button icon
│       ├── iden1.png                # Identify button icon
│       ├── noise1.png               # Noise detection icon
│       ├── exit.png                 # Exit button icon
│       ├── incognito.png            # In/Out button icon
│       ├── log.png                  # Log viewer icon
│       ├── cc1.png                  # Main logo
│       └── rectangle-of-cutted-line-geometrical-shape.png
│
├── 🎥 Motion Detection Modules
│   ├── find_motion.py               # Advanced motion detection with alerts
│   ├── motion.py                    # Basic motion detection (testing)
│   ├── rect_noise.py                # Rectangle ROI motion detection
│   └── spot_diff.py                 # Frame difference testing
│
├── 😎 Face Recognition System
│   ├── identify.py                  # Complete face recognition system
│   ├── haarcascade_frontalface_default.xml  # Haar cascade classifier
│   ├── model.yml                    # Trained LBPH model (legacy)
│   ├── enhanced_model.yml           # Enhanced LBPH model
│   ├── persons_database.json        # Person registry (ID, name, metadata)
│   └── persons/                     # Training images directory
│       └── [PersonName-ID-###.jpg]  # Face training samples
│
├── 📹 Recording & Tracking
│   ├── record.py                    # Video recording module
│   ├── in_out.py                    # Entry/exit detection
│   └── recordings/                  # Recorded videos
│       └── [DD-MM-YY-HH-MM-SS.avi]
│
├── 🔔 Alert System
│   ├── alert.py                     # Main alert dispatcher
│   ├── pushover_alert.py            # Pushover push notifications
│   ├── sms_alert.py                 # Twilio SMS alerts
│   ├── test_push.py                 # Test Pushover integration
│   └── test_sms.py                  # Test SMS integration
│
├── 📊 Logging System
│   ├── logger.py                    # Excel-based structured logging
│   ├── log_viewer.py                # Professional log viewer GUI
│   ├── alert_log.csv                # Legacy CSV logs
│   └── logs/                        # Structured logs directory
│       └── surveillance_logs.xlsx   # Main Excel log file
│
├── 📸 Captured Images
│   ├── stolen/                      # Motion detection snapshots
│   │   └── [DD-MM-YY-HH-MM-SS.jpg]
│   └── visitors/                    # Entry/exit tracking images
│       ├── in/                      # Entry snapshots
│       │   └── [DD-MM-YY-HH-MM-SS.jpg]
│       └── out/                     # Exit snapshots (to be created)
│           └── [DD-MM-YY-HH-MM-SS.jpg]
│
├── ⚙️ Configuration
│   ├── .env                         # Environment variables (not in repo)
│   ├── .env.example                 # Template for configuration
│   └── requirements.txt             # Python dependencies
│
├── 🧪 Testing & Development
│   ├── just_for_test.py             # General testing script
│   └── __pycache__/                 # Python bytecode cache
│
└── 📄 Documentation
    └── README.md                    # This file
```

### Directory Purposes:

| Directory | Purpose | Auto-Created |
|-----------|---------|--------------|
| `icons/` | GUI button images and logos | Manual |
| `persons/` | Face recognition training images | Yes |
| `stolen/` | Motion detection snapshots | Yes |
| `recordings/` | Video recordings | Yes |
| `visitors/in/` | Entry detection images | Yes |
| `visitors/out/` | Exit detection images | Yes |
| `logs/` | Excel and structured logs | Yes |
| `__pycache__/` | Python compiled bytecode | Auto |

---

## 🖥️ Interface Overview

The main GUI provides easy access to all surveillance features through a clean, icon-based interface.

### Main Interface Buttons

| Button | Icon | Feature | Description | Output |
|--------|------|---------|-------------|--------|
| 🕵️ **Monitor** | ![Monitor](icons/mon1.png) | Motion Detection | Advanced real-time motion detection with automatic alerts and snapshot capture | Images: `stolen/`, Logs: Excel/CSV |
| 😎 **Identify** | ![Identify](icons/iden1.png) | Face Recognition | Complete face training and recognition system with person management | Model: `enhanced_model.yml`, DB: `persons_database.json` |
| 🟩 **Rectangle** | ![Rectangle](icons/rectangle-of-cutted-line-geometrical-shape.png) | ROI Motion Detection | Click-and-drag custom region monitoring with real-time motion feedback | Logs: Excel (Rectangle_Motion sheet) |
| 📹 **Record** | ![Record](icons/rec1.png) | Video Recording | Records timestamped video with real-time display | Videos: `recordings/*.avi` |
| 🔄 **In/Out** | ![In/Out](icons/incognito.png) | Entry/Exit Tracking | Directional movement detection across defined zones | Images: `visitors/in/`, `visitors/out/` |
| 📋 **View Log** | ![Log](icons/log.png) | Log Viewer | Professional multi-tab log viewer with filtering, search, and export | Source: `logs/surveillance_logs.xlsx` |
| 🚪 **Exit** | ![Exit](icons/exit.png) | Application Exit | Safely closes all windows and releases camera resources | - |

### Interface Features:
- **Professional Design**: Custom icons with Tkinter GUI
- **Real-time Feedback**: Status updates and visual indicators
- **User-Friendly**: No technical knowledge required
- **System Logging**: All actions automatically logged
- **Responsive**: Optimized for smooth performance

---

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

## ⚙️ Installation & Setup

### Prerequisites
- **Python 3.10 or higher** (Download from [python.org](https://www.python.org/downloads/))
- **Webcam/Camera** (Built-in or USB camera)
- **Operating System**: Windows, macOS, or Linux

### Step 1: Clone the Repository
```bash
git clone https://github.com/Srinivas-18/Smart-home-security-audit.git
cd Smart-home-security-audit
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**OR manually install:**
```bash
pip install opencv-python opencv-contrib-python pillow python-dotenv twilio requests pandas openpyxl numpy
```

### Step 4: Set Up Environment Variables
1. Copy `.env.example` to `.env`:
   ```bash
   # Windows
   copy .env.example .env
   
   # macOS/Linux
   cp .env.example .env
   ```

2. Edit `.env` with your credentials (see [Environment Configuration](#-environment-configuration))

### Step 5: Create Required Directories
The application auto-creates directories, but you can manually create them:
```bash
# Windows PowerShell
mkdir icons, persons, stolen, recordings, logs, visitors\in, visitors\out

# macOS/Linux
mkdir -p icons persons stolen recordings logs visitors/in visitors/out
```

### Step 6: Add Icons (Optional but Recommended)
Place icon images in the `icons/` folder:
- `mon1.png` - Monitor button
- `rec1.png` - Record button
- `iden1.png` - Identify button
- `noise1.png` - Noise detection
- `exit.png` - Exit button
- `incognito.png` - In/Out button
- `log.png` - Log viewer button
- `cc1.png` - Main logo/camera icon
- `rectangle-of-cutted-line-geometrical-shape.png` - Rectangle detection

> 💡 **Tip**: If icons are missing, buttons will still work but won't display images.

### Step 7: Download Haar Cascade File
The project includes `haarcascade_frontalface_default.xml`. If missing, download from:
```bash
wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
```

### Step 8: Run the Application
```bash
python main.py
```

---

## 🔐 Environment Configuration

### Creating .env File
Create a `.env` file in the project root with the following structure:

```env
# ==========================================
# EMAIL ALERTS (SMTP Configuration)
# ==========================================
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
TO_EMAIL=receiver@example.com

# For Gmail: Enable 2FA and generate App Password
# Guide: https://support.google.com/accounts/answer/185833

# ==========================================
# TWILIO SMS ALERTS
# ==========================================
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
USER_PHONE_NUMBER=+919876543210

# Get free trial: https://www.twilio.com/try-twilio
# Format: Include country code with +

# ==========================================
# PUSHOVER PUSH NOTIFICATIONS
# ==========================================
PUSHOVER_USER_KEY=your_pushover_user_key_here
PUSHOVER_API_KEY=your_pushover_api_key_here

# Sign up: https://pushover.net/
# Create application to get API key

# ==========================================
# LOG VIEWER SECURITY
# ==========================================
LOG_USERNAME=admin
LOG_PASSWORD=1234

# Change these credentials for production use!
```

### Configuration Details

#### 1. Email Alerts (Gmail Example)
```env
EMAIL_ADDRESS=yourname@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop  # 16-character App Password
TO_EMAIL=recipient@example.com
```

**Steps to get Gmail App Password:**
1. Enable 2-Factor Authentication on your Google Account
2. Go to: https://myaccount.google.com/apppasswords
3. Select "Mail" and "Other (Custom name)"
4. Enter "Surveillance System" and click Generate
5. Copy the 16-character password (remove spaces)

#### 2. Twilio SMS
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=+15551233367  # Your Twilio number
USER_PHONE_NUMBER=+919876543210   # Your mobile number
```

**Steps:**
1. Sign up at https://www.twilio.com/try-twilio
2. Get free trial credits ($15)
3. Get a Twilio phone number
4. Copy Account SID and Auth Token from dashboard
5. Verify your personal phone number

#### 3. Pushover Notifications
```env
PUSHOVER_USER_KEY=uQiRzpo4DXghDmr9QzzfQu27cmVRsG
PUSHOVER_API_KEY=azGDORePK8gMaC0QOYAMyEEuzJnyUi
```

**Steps:**
1. Sign up at https://pushover.net/ ($5 one-time)
2. Note your User Key from dashboard
3. Create a new Application/API Token
4. Install Pushover app on your phone

#### 4. Log Security
```env
LOG_USERNAME=admin
LOG_PASSWORD=securePassword123
```

**⚠️ Important:**
- Change default credentials for production
- Never commit `.env` file to version control
- Add `.env` to `.gitignore`

### Testing Your Configuration

#### Test Email:
```python
python -c "from alert import send_email_alert; send_email_alert('Test Email')"
```

#### Test SMS:
```bash
python test_sms.py
```

#### Test Push Notification:
```bash
python test_push.py
```

---

## 🎯 Usage Guide

### First Time Setup

#### 1. Train Face Recognition System
Before using the Identify feature, you must train the system with known faces:

1. Click **"Identify"** button in main GUI
2. In the Face Recognition window, click **"Add New Person"**
3. Enter:
   - **Name**: Person's full name
   - **ID**: Unique numeric identifier (e.g., 1, 2, 3...)
4. Click **"Start Collection"**
5. Position your face in the camera frame
6. The system will collect 100 face samples (move your head slightly for different angles)
7. Training begins automatically after collection
8. Repeat for all persons you want to recognize

**Tips for Better Accuracy:**
- Ensure good lighting
- Face camera directly
- Move head slightly during capture (different angles)
- Remove glasses if possible (or train with both)
- Avoid excessive facial expressions

#### 2. Configure Alert Preferences
Edit `.env` file to enable/disable alert channels as needed.

---

### Daily Operations

#### Starting Motion Detection
1. Launch application: `python main.py`
2. Click **"Monitor"** button
3. Wait for 5-second countdown
4. System will:
   - Detect motion automatically
   - Capture snapshots when motion detected
   - Send alerts (email/SMS/push)
   - Save images to `stolen/` folder
   - Log all events to Excel
5. Press **ESC** to stop monitoring

**Motion Detection Settings:**
- Sensitivity: Auto-adjusts based on motion area
- Alert Cooldown: 5 seconds (prevents spam)
- Image Format: JPEG with timestamp in filename

---

#### Using Face Recognition
1. Click **"Identify"** button
2. Camera shows real-time feed with face detection
3. Recognized faces show:
   - **Green Box**: Known person (confidence < 80)
   - **Red Box**: Unknown person (confidence ≥ 80)
   - Name and confidence percentage displayed
4. Confidence bar shows recognition certainty
5. Press **ESC** to exit

**Managing Trained Faces:**
1. Click **"View/Manage Persons"** in Face Recognition window
2. See list of all registered persons with:
   - ID, Name, Sample count, Creation date
3. Select person and click **"Delete Selected"** to remove
4. Deletion removes:
   - Person from database
   - All training images
   - Retrains model automatically

---

#### Entry/Exit Tracking
1. Click **"In/Out"** button
2. Position camera to monitor doorway/entrance
3. **Red lines** mark detection zones:
   - Left line (x=200): Entry zone
   - Right line (x=500): Exit zone
4. When person crosses from right to left: **Entry** logged
5. When person crosses from left to right: **Exit** logged
6. Images saved to `visitors/in/` or `visitors/out/`
7. Press **ESC** to stop

**Best Practices:**
- Position camera perpendicular to doorway
- Ensure person crosses both red lines
- Good lighting required for accurate detection

---

#### Rectangle Motion Detection
For monitoring specific areas (e.g., safe, window, desk):

1. Click **"Rectangle"** button
2. **Click and drag** on camera feed to select monitoring region
3. Press **SPACE** to confirm selection
4. System monitors only the selected area for motion
5. Motion triggers:
   - Green overlay on detected region
   - Contour visualization
   - Excel logging
6. Press **ESC** to exit

**Use Cases:**
- Monitor specific object (jewelry box, computer, etc.)
- Reduce false alarms from irrelevant areas
- Focus on high-value zones

---

#### Video Recording
1. Click **"Record"** button
2. Recording starts immediately
3. Real-time timestamp overlaid on video
4. Press **ESC** to stop recording
5. Video saved to `recordings/` folder as `.avi` file
6. Duration automatically calculated and logged

**Recording Specs:**
- Format: AVI (XVID codec)
- Resolution: 640x480
- Frame Rate: 20 FPS
- Filename: `DD-MM-YY-HH-MM-SS.avi`

---

#### Viewing Logs
The system maintains comprehensive logs of all activities.

**Using Professional Log Viewer:**
1. Click **"View Log"** button in main GUI
2. Navigate tabs for different log categories:
   - **Motion Detection**: All motion events
   - **Face Recognition**: Training and recognition events
   - **Entry/Exit**: Directional movement tracking
   - **Recording**: Video recording sessions
   - **Rectangle Motion**: Custom ROI monitoring
   - **System Events**: Application lifecycle events

**Viewer Features:**
- **Filter by Date**: Today, Yesterday, Last 7/30 days, All
- **Search**: Find specific events
- **Sort**: Click column headers to sort
- **Export**: Save filtered logs to Excel/CSV
- **Context Menu**: Right-click for options:
  - Copy row data
  - Open associated image
  - Delete entry
- **Statistics**: View summary dashboard
- **Refresh**: Update with latest entries

**Legacy CSV Log Access:**
- Requires username/password authentication
- Opens `alert_log.csv` in default spreadsheet application

---

### Advanced Usage

#### Adjusting Motion Sensitivity
Edit `find_motion.py`:
```python
# Line ~80 - Change threshold values
total_motion_area > 3000  # Lower = more sensitive
motion_counter >= 2       # Lower = faster detection
```

#### Changing Alert Cooldown
Edit `find_motion.py`:
```python
# Line ~104 - Change cooldown duration
if time.time() - last_alert_time > 5:  # Change 5 to desired seconds
```

#### Face Recognition Confidence Threshold
Edit `identify.py`:
```python
# Line ~280 - Adjust confidence threshold
if confidence < 80:  # Lower = more strict, Higher = more lenient
```

---

## 🛡️ Security Features

### Authentication & Access Control
| Feature | Implementation | Purpose |
|---------|----------------|---------|
| **Log Viewer Password** | Username/password authentication | Prevents unauthorized access to surveillance logs |
| **Environment Variables** | `.env` file (gitignored) | Keeps API keys and credentials secure |
| **Credential Isolation** | Separate config file | API keys never hardcoded in source |

### Privacy & Data Protection
- **Local Storage**: All data stored locally, no cloud upload
- **Encrypted Logs**: Excel files can be password-protected manually
- **Image Timestamping**: All captures include timestamp for audit trails
- **Automatic Cleanup**: Option to implement log rotation (coming soon)

### Alert Security
- **Multi-Channel Redundancy**: If one alert channel fails, others still work
- **Rate Limiting**: 5-second cooldown prevents alert spam
- **Failure Logging**: Failed alerts logged for troubleshooting

### Camera Security
- **Exclusive Access**: Camera locked to app, prevents concurrent access
- **Resource Cleanup**: Proper camera release on exit
- **ESC Key Override**: Emergency stop available in all modules

### Surveillance Best Practices
✅ **Do's:**
- Change default log passwords
- Regularly review and clear old logs
- Test alert systems weekly
- Maintain good lighting for accurate detection
- Position cameras to respect privacy laws

❌ **Don'ts:**
- Never commit `.env` file to public repos
- Don't share log credentials
- Avoid pointing cameras at private spaces
- Don't ignore failed alert notifications

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 1. Camera Not Opening
**Error**: `❌ Failed to open camera`

**Solutions:**
```python
# Check if camera is in use by another application
# Windows: Close Skype, Teams, Zoom, etc.
# Try different camera index in code:
cap = cv2.VideoCapture(0)  # Change 0 to 1, 2, etc.
```

#### 2. Haar Cascade File Not Found
**Error**: `FileNotFoundError: haarcascade_frontalface_default.xml`

**Solution:**
Download the file:
```bash
wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
```

#### 3. Import Errors
**Error**: `ModuleNotFoundError: No module named 'cv2'`

**Solutions:**
```bash
# Reinstall OpenCV
pip uninstall opencv-python opencv-contrib-python
pip install opencv-python opencv-contrib-python

# Or use virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### 4. Alert Not Sending
**Symptoms**: Motion detected but no alerts received

**Debugging:**
1. Check `.env` file credentials
2. Test individually:
   ```bash
   python test_sms.py
   python test_push.py
   ```
3. Check console for error messages
4. Verify internet connection
5. Check Twilio/Pushover account status

#### 5. Face Recognition Not Working
**Symptoms**: Faces not detected or always showing "Unknown"

**Solutions:**
- Ensure `enhanced_model.yml` exists
- Retrain model: Delete `.yml` files and add persons again
- Check lighting conditions
- Verify camera resolution (should be at least 640x480)
- Ensure face is at least 50x50 pixels in frame

#### 6. GUI Icons Not Showing
**Symptoms**: Buttons show text but no icons

**Solutions:**
- Create `icons/` folder in project root
- Add required icon files (see [Installation](#-installation--setup))
- Icons are optional; functionality works without them

#### 7. Log Viewer Not Opening
**Error**: Excel file errors or blank log viewer

**Solutions:**
```bash
# Delete existing log file and let app recreate it
rm logs/surveillance_logs.xlsx
python main.py
# Click "View Log" to regenerate
```

#### 8. Permission Errors (Windows)
**Error**: `PermissionError: [WinError 32]`

**Solution:**
- Close Excel if `surveillance_logs.xlsx` is open
- Run as Administrator if needed
- Check folder permissions

#### 9. High CPU Usage
**Symptoms**: Computer slows down during motion detection

**Solutions:**
- Reduce camera resolution in code:
  ```python
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Lower resolution
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
  ```
- Increase frame skip interval
- Close other applications

#### 10. Twilio Free Trial Limitations
**Error**: SMS not sending to unverified numbers

**Solution:**
- Verify recipient number in Twilio console
- Upgrade to paid account ($0.0075/SMS)
- Message will include trial prefix

---

## 📊 Performance Optimization

### Motion Detection Performance
- **Frame Processing**: ~30 FPS on modern hardware
- **Lag Minimization**: 1-frame buffer, MJPEG codec
- **Background Processing**: Alerts/saving in separate thread
- **Memory Usage**: ~200-300 MB typical

### Face Recognition Performance
- **Training Time**: ~5-10 seconds for 100 samples
- **Recognition Speed**: Real-time (<50ms per frame)
- **Accuracy**: ~85-95% with good training data
- **Model Size**: ~1-5 MB depending on persons trained

### Recommended Hardware
| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | Dual-core 2.0 GHz | Quad-core 2.5+ GHz |
| **RAM** | 4 GB | 8 GB+ |
| **Camera** | 480p webcam | 720p+ webcam |
| **Storage** | 500 MB free | 2 GB+ (for recordings) |
| **OS** | Windows 10, macOS 10.14, Ubuntu 18.04 | Latest versions |

---

## 🔄 Workflow Diagrams

### Motion Detection Workflow
```
User clicks "Monitor"
    ↓
Initialize camera (640x480, 30 FPS)
    ↓
5-second countdown
    ↓
Capture reference frame
    ↓
┌─────────────────────────────────────┐
│  CONTINUOUS LOOP                     │
│  ├─ Capture current frame            │
│  ├─ Convert to grayscale             │
│  ├─ Apply Gaussian blur              │
│  ├─ Calculate frame difference       │
│  ├─ Threshold → binary image         │
│  ├─ Find contours                    │
│  ├─ Calculate total motion area      │
│  │                                    │
│  └─ IF motion_area > 3000:           │
│      ├─ Display "MOTION DETECTED!"   │
│      ├─ Queue background save        │
│      ├─ Send alerts (email/SMS/push) │
│      ├─ Log to Excel                 │
│      └─ Wait 5s cooldown             │
│                                       │
│  Update reference frame every 30     │
│  frames                              │
│  Press ESC → Exit                    │
└─────────────────────────────────────┘
```

### Face Recognition Workflow
```
┌─────────────────────────────────────┐
│  TRAINING PHASE                      │
│  ├─ User clicks "Add New Person"     │
│  ├─ Enter name and ID                │
│  ├─ Capture 100 face samples         │
│  ├─ Preprocess each sample:          │
│  │   ├─ Resize to 200x200            │
│  │   ├─ Histogram equalization       │
│  │   └─ Gaussian blur                │
│  ├─ Save to persons/ directory       │
│  ├─ Update persons_database.json     │
│  └─ Train LBPH model                 │
│      └─ Save as enhanced_model.yml   │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│  RECOGNITION PHASE                   │
│  ├─ User clicks "Start Recognition"  │
│  ├─ Load enhanced_model.yml          │
│  ├─ Capture live video frames        │
│  │                                    │
│  └─ FOR each frame:                  │
│      ├─ Detect faces (Haar Cascade)  │
│      ├─ FOR each detected face:      │
│      │   ├─ Preprocess face region   │
│      │   ├─ Predict using LBPH       │
│      │   ├─ Get person_id & confidence│
│      │   │                            │
│      │   └─ IF confidence < 80:      │
│      │       ├─ Lookup name from DB  │
│      │       ├─ Draw green box       │
│      │       └─ Display name          │
│      │     ELSE:                      │
│      │       ├─ Draw red box          │
│      │       └─ Display "Unknown"     │
│      │                                │
│      └─ Press ESC → Exit             │
└─────────────────────────────────────┘
```

---

## 📈 Data Flow Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      INPUT LAYER                              │
│  [Webcam/Camera] → OpenCV VideoCapture                       │
└────────────────────────┬─────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┬──────────────┐
         │               │               │              │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐   ┌────▼─────┐
    │ Motion  │    │  Face   │    │ Entry/  │   │ Video    │
    │ Detect  │    │  Recog  │    │  Exit   │   │ Record   │
    └────┬────┘    └────┬────┘    └────┬────┘   └────┬─────┘
         │              │              │             │
         └──────────────┼──────────────┼─────────────┘
                        │              │
                   ┌────▼──────────────▼────┐
                   │   PROCESSING LAYER      │
                   │  ├─ Image Processing    │
                   │  ├─ Feature Extraction  │
                   │  ├─ Pattern Recognition │
                   │  └─ Event Detection     │
                   └────┬────────────────────┘
                        │
         ┌──────────────┼──────────────┬──────────────┐
         │              │              │              │
    ┌────▼────┐    ┌───▼─────┐   ┌───▼────┐    ┌───▼─────┐
    │ Storage │    │ Alerting│   │Logging │    │ Display │
    │  Layer  │    │  Layer  │   │ Layer  │    │  Layer  │
    └─────────┘    └─────────┘   └────────┘    └─────────┘
         │              │              │             │
    ┌────▼────┐    ┌───▼─────┐   ┌───▼────┐    ┌───▼─────┐
    │ Images: │    │ Email   │   │ Excel  │    │ GUI     │
    │ stolen/ │    │ SMS     │   │ CSV    │    │ Windows │
    │visitors/│    │ Push    │   │ JSON   │    │ Frames  │
    │ persons/│    └─────────┘   └────────┘    └─────────┘
    │recordings│
    └─────────┘
```

---

## 💡 Future Enhancements

### Planned Features (Roadmap)

#### Phase 1: Cloud Integration
- [ ] **Google Drive Sync** - Auto-upload captured images to Google Drive
- [ ] **Firebase Storage** - Real-time cloud backup of all surveillance data
- [ ] **Azure Blob Storage** - Enterprise-grade cloud storage integration
- [ ] **Dropbox Integration** - Alternative cloud storage option

#### Phase 2: Enhanced Communication
- [ ] **Telegram Bot** - Instant alerts via Telegram with image preview
- [ ] **WhatsApp Integration** - Send alerts through WhatsApp Business API
- [ ] **Discord Webhooks** - Notifications to Discord channels
- [ ] **Slack Integration** - Workplace security alerts

#### Phase 3: Web Dashboard
- [ ] **Streamlit Dashboard** - Real-time monitoring web interface
  - Live camera feed streaming
  - Historical data visualization
  - Interactive charts and graphs
  - Remote system control
- [ ] **Flask REST API** - Backend API for mobile apps
- [ ] **React.js Frontend** - Professional web interface
- [ ] **Mobile Apps** - iOS and Android native apps

#### Phase 4: Advanced AI Features
- [ ] **Object Detection (YOLO)** - Detect specific objects:
  - Weapons (guns, knives)
  - Bags and backpacks
  - Vehicles (cars, bikes)
  - Animals (pets vs. intruders)
- [ ] **Person Re-identification** - Track same person across multiple cameras
- [ ] **Crowd Detection** - Alert on unusual crowd gathering
- [ ] **Behavior Analysis** - Detect suspicious behaviors:
  - Loitering
  - Running
  - Fighting
  - Falling (elderly care)

#### Phase 5: Enhanced Security
- [ ] **Multi-User System** - Role-based access control:
  - Admin (full access)
  - Security (view-only)
  - Resident (limited alerts)
- [ ] **Database Encryption** - AES-256 encryption for all logs
- [ ] **Biometric Login** - Fingerprint/face authentication for app access
- [ ] **Audit Trails** - Complete activity logging for compliance

#### Phase 6: Hardware Integration
- [ ] **Multi-Camera Support** - Monitor multiple cameras simultaneously
- [ ] **PTZ Camera Control** - Pan-Tilt-Zoom camera integration
- [ ] **Raspberry Pi Support** - Deploy on edge devices
- [ ] **NVIDIA Jetson Optimization** - GPU-accelerated processing
- [ ] **IoT Integration** - Control smart locks, lights, alarms

#### Phase 7: Intelligent Alerting
- [ ] **Smart Notifications** - AI-based alert prioritization
- [ ] **Geofencing** - Disable alerts when owner is home
- [ ] **Schedule-based Monitoring** - Auto-enable during specific hours
- [ ] **Zone-based Alerts** - Different alert rules for different areas
- [ ] **False Positive Reduction** - Machine learning to reduce false alarms

#### Phase 8: Analytics & Reporting
- [ ] **Weekly Reports** - Automated summary emails
- [ ] **Activity Heatmaps** - Visual representation of motion patterns
- [ ] **Visitor Analytics** - Track entry/exit patterns
- [ ] **Face Recognition Stats** - Most frequent visitors
- [ ] **Export to PDF** - Professional incident reports

#### Phase 9: Scalability
- [ ] **Docker Containerization** - Easy deployment
- [ ] **Kubernetes Support** - Scale to multiple locations
- [ ] **Load Balancing** - Handle multiple camera streams
- [ ] **Database Migration** - PostgreSQL/MongoDB for large deployments

#### Phase 10: Compliance & Legal
- [ ] **GDPR Compliance** - Data privacy features
- [ ] **Automatic Data Deletion** - Configurable retention policies
- [ ] **Privacy Masking** - Blur faces in non-critical areas
- [ ] **Legal Templates** - Privacy policy and consent forms

---

### Community Requested Features
Vote for features by opening issues on GitHub!

- [ ] **Time-lapse Recording** - Create time-lapse videos
- [ ] **Sound Detection** - Alert on glass breaking, shouting
- [ ] **License Plate Recognition** - Vehicle tracking
- [ ] **Thermal Camera Support** - Night vision monitoring
- [ ] **Weather Integration** - Correlate events with weather data

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

1. **Report Bugs** 🐛
   - Open an issue on GitHub
   - Include OS, Python version, and error logs
   - Provide steps to reproduce

2. **Suggest Features** 💡
   - Open a feature request issue
   - Explain use case and benefits
   - Include mockups if possible

3. **Submit Code** 💻
   - Fork the repository
   - Create a feature branch (`git checkout -b feature/AmazingFeature`)
   - Commit changes (`git commit -m 'Add AmazingFeature'`)
   - Push to branch (`git push origin feature/AmazingFeature`)
   - Open a Pull Request

4. **Improve Documentation** 📝
   - Fix typos and unclear sections
   - Add tutorials and guides
   - Create video demonstrations

5. **Test & Review** 🧪
   - Test on different platforms
   - Review pull requests
   - Provide feedback on issues

### Development Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Smart-home-security-audit.git
cd Smart-home-security-audit

# Add upstream remote
git remote add upstream https://github.com/Srinivas-18/Smart-home-security-audit.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install in development mode
pip install -r requirements.txt
pip install pytest black flake8  # Development tools

# Run tests (when available)
pytest tests/

# Format code
black *.py

# Check code style
flake8 *.py
```

### Code Style Guidelines
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic
- Keep functions focused and small

### Pull Request Guidelines
- Update README.md if needed
- Add tests for new features
- Ensure all tests pass
- Update requirements.txt if adding dependencies
- Link related issues

---

## 📞 Support & Contact

### Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/Srinivas-18/Smart-home-security-audit/issues)
- **Discussions**: [Ask questions and share ideas](https://github.com/Srinivas-18/Smart-home-security-audit/discussions)
- **Email**: Contact authors directly (see [Authors](#-authors))

### Frequently Asked Questions (FAQ)

**Q: Can I use this for commercial purposes?**
A: Yes, but you must give proper credit as per MIT License terms.

**Q: How many cameras can I connect?**
A: Currently supports one camera. Multi-camera support is planned.

**Q: Does it work on Raspberry Pi?**
A: Yes, with Python 3.10+ and OpenCV installed. Performance may vary.

**Q: Can I run this 24/7?**
A: Yes, but implement log rotation and disk space monitoring.

**Q: Is internet required?**
A: Only for alerts (email/SMS/push). Core functionality works offline.

**Q: How accurate is face recognition?**
A: 85-95% with good training data (100 samples per person).

**Q: Can it detect at night?**
A: Requires adequate lighting or infrared camera.

**Q: How much disk space needed?**
A: ~10 MB per hour of snapshots, ~500 MB per hour of video.

---

## 🏆 Acknowledgments

### Technologies Used
- **OpenCV** - Computer vision library
- **Python** - Programming language
- **Tkinter** - GUI framework
- **Twilio** - SMS API provider
- **Pushover** - Push notification service

### Inspirations
- Home security needs during COVID-19 lockdown
- Open-source surveillance projects
- Community feedback and suggestions

### Special Thanks
- OpenCV community for excellent documentation
- Stack Overflow contributors
- Beta testers and early adopters
- GitHub sponsors and supporters

---

## 📜 Version History

### v2.0 (Current) - December 2025
- ✨ Complete rewrite with modular architecture
- ✨ Professional Excel-based logging system
- ✨ Enhanced GUI with log viewer
- ✨ Improved face recognition accuracy
- ✨ Multi-threaded alert processing
- ✨ Rectangle motion detection
- ✨ Entry/exit tracking
- 🐛 Fixed camera lag issues
- 🐛 Resolved memory leaks
- 📝 Comprehensive documentation

### v1.0 - 2024
- 🎉 Initial release
- ✨ Basic motion detection
- ✨ Face recognition
- ✨ Email alerts
- ✨ CSV logging

---

## 🔒 Privacy & Legal

### Privacy Policy
This software:
- Stores all data locally on your device
- Does not transmit data to third parties (except configured alert services)
- You control all collected data
- No analytics or tracking implemented

### Legal Disclaimer
⚠️ **Important**: Users are responsible for:
- Complying with local surveillance laws
- Obtaining consent when required
- Respecting privacy rights
- Securing stored footage
- Not using for illegal purposes

**The authors assume no liability for misuse of this software.**

### Compliance Notes
- **GDPR (Europe)**: Implement data retention policies
- **CCPA (California)**: Provide data access and deletion
- **Recording Laws**: Check if audio recording is legal in your jurisdiction
- **Workplace**: Get employee consent before deployment

### Recommended Practices
1. Post visible "Video Surveillance" signs
2. Limit camera field of view to your property
3. Implement automatic data deletion (30-90 days)
4. Secure logs with strong passwords
5. Regularly review and delete unnecessary footage

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐ on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=Srinivas-18/Smart-home-security-audit&type=Date)](https://star-history.com/#Srinivas-18/Smart-home-security-audit&Date)

---

## 🙌 Authors

**VARIGONDA LAKSHMI SRINIVAS**  
🔗 [GitHub → Srinivas-18](https://github.com/Srinivas-18)  
📧 Email: [Contact via GitHub]

**PATTEL PRANAY REDDY**  
🔗 [GitHub → pranay-04](https://github.com/pranay-04)  
📧 Email: [Contact via GitHub]

---

## 📄 License

MIT License - © 2025 VARIGONDA LAKSHMI SRINIVAS & PATTEL PRANAY REDDY

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

**The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.**

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 🎯 Project Stats

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-Latest-green)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success)
![Maintenance](https://img.shields.io/badge/Maintained-Yes-brightgreen)

---

## 🔗 Related Projects

- [Motion](https://github.com/Motion-Project/motion) - Advanced motion detection
- [ZoneMinder](https://github.com/ZoneMinder/zoneminder) - Full video security system
- [Shinobi](https://gitlab.com/Shinobi-Systems/Shinobi) - Open-source CCTV software
- [MotionEye](https://github.com/ccrisan/motioneye) - Web-based surveillance solution

---

<div align="center">

### ⭐ Star this repo if you like it • Fork if you want to build on it • PRs welcome!

**Made with ❤️ by Srinivas & Pranay**

[🔝 Back to Top](#-smart-surveillance-system-20)

</div>

