import cv2 
import numpy as np
from logger import surveillance_logger

# Enhanced Rectangle Motion Detection
class RectangleMotionDetector:
    def __init__(self):
        self.selecting = False
        self.selected = False
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0
        self.temp_x, self.temp_y = 0, 0
    
    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.selecting = True
            self.selected = False
            self.x1, self.y1 = x, y
            self.temp_x, self.temp_y = x, y
            
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.selecting:
                self.temp_x, self.temp_y = x, y
                
        elif event == cv2.EVENT_LBUTTONUP:
            self.selecting = False
            self.selected = True
            self.x2, self.y2 = x, y
            
            # Ensure coordinates are in correct order
            if self.x1 > self.x2:
                self.x1, self.x2 = self.x2, self.x1
            if self.y1 > self.y2:
                self.y1, self.y2 = self.y2, self.y1
    
    def draw_selection(self, frame):
        """Draw the selection rectangle"""
        if self.selecting:
            # Draw temporary rectangle while selecting
            cv2.rectangle(frame, (self.x1, self.y1), (self.temp_x, self.temp_y), (255, 255, 0), 2)
        elif self.selected:
            # Draw final selected rectangle
            cv2.rectangle(frame, (self.x1, self.y1), (self.x2, self.y2), (0, 0, 255), 2)
            # Add corner markers
            cv2.circle(frame, (self.x1, self.y1), 5, (0, 255, 0), -1)
            cv2.circle(frame, (self.x2, self.y2), 5, (0, 255, 0), -1)
        
        return frame

def rect_noise():
    detector = RectangleMotionDetector()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Cannot access camera")
        return
    
    # Selection phase
    cv2.namedWindow("Select Region - Click and drag to select area", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("Select Region - Click and drag to select area", detector.mouse_callback)
    
    print("Instructions:")
    print("1. Click and drag to select the monitoring region")
    print("2. Press SPACE to confirm selection")
    print("3. Press ESC to exit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read from camera")
            break
        
        # Draw selection rectangle and instructions
        frame = detector.draw_selection(frame)
        
        # Add instructions on frame
        cv2.putText(frame, "Click and drag to select region", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Press SPACE to confirm, ESC to exit", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if detector.selected:
            cv2.putText(frame, "Region selected! Press SPACE to start monitoring", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow("Select Region - Click and drag to select area", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            cap.release()
            cv2.destroyAllWindows()
            return
        elif key == 32 and detector.selected:  # SPACE
            break
    
    cv2.destroyAllWindows()
    
    # Validate selection
    if not detector.selected or detector.x1 == detector.x2 or detector.y1 == detector.y2:
        print("Invalid selection. Please select a proper rectangle.")
        cap.release()
        return
    
    print(f"Monitoring region: ({detector.x1}, {detector.y1}) to ({detector.x2}, {detector.y2})")
    
    # Motion detection phase
    cv2.namedWindow("Rectangle Motion Detection - ESC to exit", cv2.WINDOW_AUTOSIZE)
    
    # Get initial frame for background subtraction
    ret, prev_frame = cap.read()
    if not ret:
        cap.release()
        return
    
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_roi = prev_gray[detector.y1:detector.y2, detector.x1:detector.x2]
    
    motion_threshold = 1000  # Adjust sensitivity
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Extract current ROI
        current_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        current_roi = current_gray[detector.y1:detector.y2, detector.x1:detector.x2]
        
        # Check if ROI is valid
        if current_roi.size == 0 or prev_roi.size == 0:
            cv2.putText(frame, "Invalid region selected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            # Calculate difference
            diff = cv2.absdiff(current_roi, prev_roi)
            
            # Apply blur and threshold
            diff = cv2.GaussianBlur(diff, (5, 5), 0)
            _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Calculate total motion area
            total_motion_area = sum(cv2.contourArea(c) for c in contours)
            
            # Draw monitoring rectangle
            cv2.rectangle(frame, (detector.x1, detector.y1), (detector.x2, detector.y2), (0, 0, 255), 2)
            
            if total_motion_area > motion_threshold:
                # Motion detected
                cv2.putText(frame, "MOTION DETECTED!", (10, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                
                # Log rectangle motion detection
                surveillance_logger.log_rectangle_motion(
                    region=f"Custom_{detector.x1}_{detector.y1}_{detector.x2}_{detector.y2}",
                    motion_area=int(total_motion_area),
                    status="motion_detected",
                    coordinates=f"({detector.x1},{detector.y1})-({detector.x2},{detector.y2})",
                    sensitivity="high" if total_motion_area > motion_threshold * 2 else "medium"
                )
                
                # Draw motion contours in the ROI
                for contour in contours:
                    if cv2.contourArea(contour) > 100:  # Filter small contours
                        x, y, w, h = cv2.boundingRect(contour)
                        # Adjust coordinates to full frame
                        cv2.rectangle(frame, (x + detector.x1, y + detector.y1), 
                                    (x + w + detector.x1, y + h + detector.y1), (0, 255, 0), 2)
                
                # Fill monitoring rectangle with semi-transparent green
                overlay = frame.copy()
                cv2.rectangle(overlay, (detector.x1, detector.y1), (detector.x2, detector.y2), (0, 255, 0), -1)
                cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
                
            else:
                # No motion
                cv2.putText(frame, "NO MOTION", (10, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
            # Show motion sensitivity info
            cv2.putText(frame, f"Motion Area: {int(total_motion_area)}", (10, 80), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Update previous frame
            prev_roi = current_roi.copy()
        
        # Add instructions
        cv2.putText(frame, "Press ESC to exit", (10, frame.shape[0] - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow("Rectangle Motion Detection - ESC to exit", frame)
        
        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Rectangle motion detection stopped.")
 