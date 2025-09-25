import cv2
import time
import os
from datetime import datetime
from alert import send_all_alerts
import csv
import threading
from queue import Queue
from logger import surveillance_logger

os.makedirs("stolen", exist_ok=True)
log_file = "alert_log.csv"

if not os.path.exists(log_file):
    with open(log_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Image", "Alert Message"])

# Background worker for heavy operations
def background_worker(task_queue):
    """Process heavy operations in background thread"""
    while True:
        try:
            task = task_queue.get(timeout=1)
            if task is None:  # Shutdown signal
                break
            
            task_type, data = task
            
            if task_type == "save_and_alert":
                timestamp, filename, frame, alert_msg = data
                
                # Save image (heavy operation)
                cv2.imwrite(filename, frame)
                
                # Send alerts (heavy network operations)
                try:
                    send_all_alerts(alert_msg)
                    print(f"✅ Alert sent! Snapshot saved: {filename}")
                except Exception as e:
                    print(f"⚠️ Alert failed: {e}")
                
                # Log to CSV (file I/O)
                try:
                    with open(log_file, 'a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow([timestamp, filename, alert_msg])
                except Exception as e:
                    print(f"⚠️ Logging failed: {e}")
            
            task_queue.task_done()
            
        except:
            continue  # Timeout or other error, keep running

def find_motion():
    # Initialize background task queue and worker thread
    task_queue = Queue()
    worker_thread = threading.Thread(target=background_worker, args=(task_queue,), daemon=True)
    worker_thread.start()
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Failed to open camera.")
        task_queue.put(None)  # Shutdown worker
        return

    # Aggressive camera optimization for minimal lag
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Critical: minimize buffer lag
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))  # Use MJPEG for speed

    countdown_start = time.time()
    countdown_duration = 5  # 5 second countdown as requested

    print("🎥 Initializing lag-free motion detection...")
    
    # Quick countdown with minimal processing
    while time.time() - countdown_start < countdown_duration:
        ret, frame = cap.read()
        if not ret:
            continue
        
        remaining = int(countdown_duration - (time.time() - countdown_start))
        if remaining > 0:
            cv2.putText(frame, f"Starting in {remaining}s", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.imshow("Motion Detection - ESC to exit", frame)
            if cv2.waitKey(1) == 27:
                cap.release()
                cv2.destroyAllWindows()
                task_queue.put(None)
                return

    # Get initial reference frame with minimal processing
    ret, reference_frame = cap.read()
    if not ret:
        cap.release()
        task_queue.put(None)
        return
    
    # Simplified preprocessing for speed
    reference_gray = cv2.cvtColor(reference_frame, cv2.COLOR_BGR2GRAY)
    reference_gray = cv2.GaussianBlur(reference_gray, (15, 15), 0)  # Reduced blur size
    
    last_alert_time = 0
    motion_detected = False
    motion_counter = 0
    no_motion_counter = 0
    frame_skip = 0  # Skip frames for performance
    
    print("✅ Lag-free motion detection started!")

    try:
        while True:
            ret, current_frame = cap.read()
            if not ret:
                continue

            # Skip every other frame for better performance
            frame_skip += 1
            if frame_skip % 2 == 0:
                continue

            # Minimal processing - work directly on current frame
            current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
            current_gray = cv2.GaussianBlur(current_gray, (15, 15), 0)
            
            # Fast frame difference calculation
            frame_delta = cv2.absdiff(reference_gray, current_gray)
            thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)[1]
            
            # Minimal morphological operations
            thresh = cv2.dilate(thresh, None, iterations=1)
            
            # Fast contour detection
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Quick area calculation
            total_motion_area = sum(cv2.contourArea(c) for c in contours if cv2.contourArea(c) > 800)
            
            # Simplified motion logic
            if total_motion_area > 3000:
                motion_counter += 1
                no_motion_counter = 0
                if motion_counter >= 2:  # Faster response
                    motion_detected = True
            else:
                no_motion_counter += 1
                motion_counter = 0
                if no_motion_counter >= 3:  # Faster clear
                    motion_detected = False

            # Minimal display processing
            if motion_detected:
                cv2.putText(current_frame, "MOTION DETECTED!", (30, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                cv2.putText(current_frame, f"Area: {int(total_motion_area)}", (30, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Non-blocking alert processing
                if time.time() - last_alert_time > 5:
                    timestamp = datetime.now().strftime('%d-%m-%y %H:%M:%S')
                    filename = f"stolen/{datetime.now().strftime('%d-%m-%y-%H-%M-%S')}.jpg"
                    alert_msg = "🚨 Motion detected in surveillance area!"
                    
                    # Queue heavy operations for background processing
                    task_queue.put(("save_and_alert", (timestamp, filename, current_frame.copy(), alert_msg)))
                    
                    # Log motion detection event
                    surveillance_logger.log_motion_detection(
                        status="motion_detected",
                        motion_area=int(total_motion_area),
                        alert_sent=True,
                        image_path=filename,
                        sensitivity="high" if total_motion_area > 5000 else "medium"
                    )
                    
                    last_alert_time = time.time()
                    print("📤 Alert queued for background processing")
            else:
                cv2.putText(current_frame, "NO MOTION", (30, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                cv2.putText(current_frame, "Monitoring...", (30, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Minimal UI elements
            cv2.putText(current_frame, "Press ESC to exit", 
                       (30, current_frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Update reference frame less frequently
            if frame_skip % 60 == 0:  # Every 30 frames instead of time-based
                reference_gray = current_gray.copy()

            cv2.imshow("Motion Detection - ESC to exit", current_frame)

            # Minimal key processing
            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        task_queue.put(None)  # Shutdown background worker
        print("🛑 Motion detection stopped.")
