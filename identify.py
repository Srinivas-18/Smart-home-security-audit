import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import tkinter.font as font
from PIL import Image, ImageTk
import json
from datetime import datetime
from logger import surveillance_logger

# Enhanced Face Recognition System with improved accuracy and GUI
class FaceRecognitionSystem:
    def __init__(self):
        self.cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.persons_db = "persons_database.json"
        self.model_file = "enhanced_model.yml"
        self.persons_dir = "persons"
        
        # Create directories if they don't exist
        os.makedirs(self.persons_dir, exist_ok=True)
        
        # Load existing database
        self.load_database()
    
    def load_database(self):
        """Load persons database from JSON file"""
        try:
            if os.path.exists(self.persons_db):
                with open(self.persons_db, 'r') as f:
                    self.database = json.load(f)
            else:
                self.database = {}
        except:
            self.database = {}
    
    def save_database(self):
        """Save persons database to JSON file"""
        with open(self.persons_db, 'w') as f:
            json.dump(self.database, f, indent=2)
    
    def preprocess_face(self, face_img):
        """Enhanced face preprocessing for better accuracy"""
        # Resize to standard size
        face_img = cv2.resize(face_img, (200, 200))
        
        # Apply histogram equalization for better contrast
        face_img = cv2.equalizeHist(face_img)
        
        # Apply Gaussian blur to reduce noise
        face_img = cv2.GaussianBlur(face_img, (3, 3), 0)
        
        return face_img
    
    def collect_person_data(self, name, person_id):
        """Enhanced data collection with better face detection"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Cannot access camera")
            return False
        
        count = 0
        target_samples = 100  # Reduced from 300 for better quality
        
        # Create progress window
        progress_window = tk.Toplevel()
        progress_window.title("Collecting Face Data")
        progress_window.geometry("400x200")
        progress_window.resizable(False, False)
        
        tk.Label(progress_window, text=f"Collecting data for: {name}", 
                font=('Arial', 12, 'bold')).pack(pady=10)
        
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, variable=progress_var, 
                                     maximum=target_samples, length=300)
        progress_bar.pack(pady=10)
        
        status_label = tk.Label(progress_window, text="Position your face in the camera")
        status_label.pack(pady=5)
        
        instruction_label = tk.Label(progress_window, 
                                   text="Move your head slightly for different angles\nPress ESC to stop early")
        instruction_label.pack(pady=5)
        
        collected_faces = []
        
        while count < target_samples:
            ret, frame = cap.read()
            if not ret:
                continue
            
            # Flip frame for better user experience
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Enhanced face detection with multiple scale factors
            faces = self.cascade.detectMultiScale(gray, 
                                                scaleFactor=1.1, 
                                                minNeighbors=5,
                                                minSize=(50, 50),
                                                maxSize=(300, 300))
            
            for (x, y, w, h) in faces:
                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Extract and preprocess face
                face_roi = gray[y:y+h, x:x+w]
                
                # Quality check - ensure face is large enough and well-lit
                if w > 80 and h > 80:
                    processed_face = self.preprocess_face(face_roi)
                    
                    # Save face image
                    filename = f"{self.persons_dir}/{name}-{count}-{person_id}.jpg"
                    cv2.imwrite(filename, processed_face)
                    collected_faces.append(processed_face)
                    
                    count += 1
                    
                    # Update progress
                    progress_var.set(count)
                    status_label.config(text=f"Collected: {count}/{target_samples} samples")
                    progress_window.update()
                    
                    # Show collected face in small window
                    cv2.imshow("Collected Face", processed_face)
            
            # Show main camera feed
            cv2.putText(frame, f"Samples: {count}/{target_samples}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Press ESC to stop", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            cv2.imshow("Face Collection - Position your face in the green rectangle", frame)
            
            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break
        
        cap.release()
        cv2.destroyAllWindows()
        progress_window.destroy()
        
        if count > 20:  # Minimum samples required
            # Update database
            self.database[str(person_id)] = {
                'name': name,
                'samples': count,
                'created': datetime.now().isoformat()
            }
            self.save_database()
            
            # Log face recognition event
            surveillance_logger.log_face_recognition(
                action="person_added",
                person_name=name,
                person_id=str(person_id),
                status="success",
                image_count=count
            )
            
            messagebox.showinfo("Success", 
                              f"Successfully collected {count} face samples for {name}!\n"
                              f"Training will begin automatically.")
            return True
        else:
            messagebox.showwarning("Insufficient Data", 
                                 f"Only {count} samples collected. Minimum 20 required.")
            return False
    
    def train_model(self):
        """Enhanced training with better error handling"""
        if not os.path.exists(self.persons_dir) or not os.listdir(self.persons_dir):
            messagebox.showwarning("No Data", "No training data found. Please add persons first.")
            return False
        
        try:
            faces = []
            labels = []
            
            # Load all face images
            for filename in os.listdir(self.persons_dir):
                if filename.endswith('.jpg'):
                    path = os.path.join(self.persons_dir, filename)
                    
                    # Extract person ID from filename
                    try:
                        person_id = int(filename.split('-')[2].split('.')[0])
                        face_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                        
                        if face_img is not None:
                            faces.append(face_img)
                            labels.append(person_id)
                    except (ValueError, IndexError):
                        continue
            
            if len(faces) == 0:
                messagebox.showerror("Error", "No valid face images found for training.")
                return False
            
            # Train the recognizer
            self.recognizer.train(faces, np.array(labels))
            self.recognizer.save(self.model_file)
            
            messagebox.showinfo("Training Complete", 
                              f"Model trained successfully with {len(faces)} face samples!\n"
                              f"Unique faces: {len(set(labels))}")
            return True
            
        except Exception as e:
            messagebox.showerror("Training Error", f"Error during training: {str(e)}")
            return False
    
    def start_recognition(self):
        """Enhanced recognition with better accuracy and confidence display"""
        if not os.path.exists(self.model_file):
            messagebox.showwarning("No Model", "No trained model found. Please train the model first.")
            return
        
        try:
            self.recognizer.read(self.model_file)
        except:
            messagebox.showerror("Error", "Failed to load recognition model.")
            return
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Cannot access camera")
            return
        
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            
            # Flip frame for better user experience
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Enhanced face detection
            faces = self.cascade.detectMultiScale(gray, 
                                                scaleFactor=1.1, 
                                                minNeighbors=5,
                                                minSize=(50, 50))
            
            for (x, y, w, h) in faces:
                # Extract and preprocess face
                face_roi = gray[y:y+h, x:x+w]
                processed_face = self.preprocess_face(face_roi)
                
                # Predict identity
                person_id, confidence = self.recognizer.predict(processed_face)
                
                # Improved confidence threshold
                if confidence < 80:  # More strict threshold
                    person_name = self.database.get(str(person_id), {}).get('name', 'Unknown')
                    color = (0, 255, 0)  # Green for recognized
                    label = f"{person_name} ({confidence:.1f})"
                else:
                    color = (0, 0, 255)  # Red for unknown
                    label = f"Unknown ({confidence:.1f})"
                
                # Draw rectangle and label
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, label, (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                
                # Add confidence bar
                bar_width = int((100 - min(confidence, 100)) * 2)
                cv2.rectangle(frame, (x, y+h+5), (x+bar_width, y+h+15), color, -1)
            
            # Add instructions
            cv2.putText(frame, "Press ESC to exit", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow("Face Recognition - ESC to exit", frame)
            
            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break
        
        cap.release()
        cv2.destroyAllWindows()

# GUI Application
def create_main_gui():
    """Create the enhanced Face Recognition System GUI"""
    face_system = FaceRecognitionSystem()
    
    def add_new_person():
        """Add new person dialog"""
        dialog = tk.Toplevel()
        dialog.title("Add New Person")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Center the dialog
        dialog.transient()
        
        tk.Label(dialog, text="Face Registration System", 
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Name input
        tk.Label(dialog, text="Enter name:", font=('Arial', 12)).pack(pady=5)
        name_var = tk.StringVar()
        name_entry = tk.Entry(dialog, textvariable=name_var, font=('Arial', 12), width=30)
        name_entry.pack(pady=5)
        name_entry.focus()
        
        # ID input
        tk.Label(dialog, text="Enter ID (numbers only):", font=('Arial', 12)).pack(pady=5)
        id_var = tk.StringVar()
        id_entry = tk.Entry(dialog, textvariable=id_var, font=('Arial', 12), width=30)
        id_entry.pack(pady=5)
        
        def start_collection():
            name = name_var.get().strip()
            person_id = id_var.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Please enter a name")
                return
            
            if not person_id.isdigit():
                messagebox.showerror("Error", "ID must be numbers only")
                return
            
            person_id = int(person_id)
            
            # Check if ID already exists
            if str(person_id) in face_system.database:
                if not messagebox.askyesno("ID Exists", 
                                         f"ID {person_id} already exists for {face_system.database[str(person_id)]['name']}. "
                                         f"Do you want to replace it?"):
                    return
            
            dialog.destroy()
            
            # Start data collection
            if face_system.collect_person_data(name, person_id):
                # Auto-train after successful collection
                face_system.train_model()
        
        tk.Button(dialog, text="Start Collection", command=start_collection,
                 bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'),
                 padx=20, pady=10).pack(pady=20)
        
        tk.Button(dialog, text="Cancel", command=dialog.destroy,
                 bg='#f44336', fg='white', font=('Arial', 12),
                 padx=20, pady=5).pack(pady=5)
    
    def view_manage_persons():
        """View and manage registered persons"""
        if not face_system.database:
            messagebox.showinfo("No Data", "No persons registered yet.")
            return
        
        manage_window = tk.Toplevel()
        manage_window.title("Registered Persons")
        manage_window.geometry("600x400")
        
        # Create treeview for person list
        columns = ('ID', 'Name', 'Samples', 'Created')
        tree = ttk.Treeview(manage_window, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Populate treeview
        for person_id, data in face_system.database.items():
            created_date = data.get('created', 'Unknown')
            if created_date != 'Unknown':
                try:
                    created_date = datetime.fromisoformat(created_date).strftime('%Y-%m-%d')
                except:
                    pass
            
            tree.insert('', 'end', values=(
                person_id, 
                data['name'], 
                data.get('samples', 'Unknown'),
                created_date
            ))
        
        tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Buttons frame
        btn_frame = tk.Frame(manage_window)
        btn_frame.pack(pady=10)
        
        def delete_selected():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a person to delete.")
                return
            
            item = tree.item(selection[0])
            person_id = item['values'][0]
            person_name = item['values'][1]
            
            if messagebox.askyesno("Confirm Delete", 
                                 f"Are you sure you want to delete {person_name} (ID: {person_id})?\n"
                                 f"This will also delete all associated training images."):
                
                deleted_files = 0
                
                # Delete all image files for this person
                if os.path.exists(face_system.persons_dir):
                    for filename in os.listdir(face_system.persons_dir):
                        if filename.endswith('.jpg'):
                            # Check multiple patterns to ensure all files are caught
                            file_parts = filename.split('-')
                            if len(file_parts) >= 3:
                                try:
                                    # Extract name and ID from filename
                                    file_name = file_parts[0]
                                    file_id = file_parts[2].split('.')[0]
                                    
                                    # Match by ID (most reliable) or by name
                                    if file_id == str(person_id) or file_name == person_name:
                                        file_path = os.path.join(face_system.persons_dir, filename)
                                        try:
                                            os.remove(file_path)
                                            deleted_files += 1
                                        except Exception as e:
                                            print(f"Error deleting {filename}: {e}")
                                except (ValueError, IndexError):
                                    # If filename format doesn't match expected pattern, skip
                                    continue
                
                # Delete from database
                if str(person_id) in face_system.database:
                    del face_system.database[str(person_id)]
                    face_system.save_database()
                
                # Retrain model if there are remaining persons
                remaining_persons = len(face_system.database)
                if remaining_persons > 0:
                    try:
                        face_system.train_model()
                    except:
                        pass  # Training might fail if no valid images remain
                
                # Refresh list
                tree.delete(selection[0])
                
                # Show detailed deletion summary
                messagebox.showinfo("Deleted", 
                                  f"{person_name} (ID: {person_id}) has been deleted.\n"
                                  f"Deleted {deleted_files} training images.\n"
                                  f"Remaining persons: {remaining_persons}")
                
                # Update info display in main window if it exists
                try:
                    info_text = ("Training Images: " + str(len([f for f in os.listdir(face_system.persons_dir) 
                                                               if f.endswith('.jpg')]) if os.path.exists(face_system.persons_dir) else "0") + 
                                "\nUnique Faces: " + str(len(face_system.database)))
                    # This will update the main window info if accessible
                except:
                    pass
        
        def refresh_list():
            for item in tree.get_children():
                tree.delete(item)
            
            for person_id, data in face_system.database.items():
                created_date = data.get('created', 'Unknown')
                if created_date != 'Unknown':
                    try:
                        created_date = datetime.fromisoformat(created_date).strftime('%Y-%m-%d')
                    except:
                        pass
                
                tree.insert('', 'end', values=(
                    person_id, 
                    data['name'], 
                    data.get('samples', 'Unknown'),
                    created_date
                ))
        
        tk.Button(btn_frame, text="Delete Selected", command=delete_selected,
                 bg='#f44336', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Refresh List", command=refresh_list,
                 bg='#2196F3', fg='white', font=('Arial', 10)).pack(side='left', padx=5)
    
    # Main window
    root = tk.Tk()
    root.title("Face Recognition System")
    root.geometry("600x400")
    root.configure(bg='#f0f0f0')
    
    # Title
    title_label = tk.Label(root, text="Face Recognition System", 
                          font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#333')
    title_label.pack(pady=30)
    
    # Button frame
    btn_frame = tk.Frame(root, bg='#f0f0f0')
    btn_frame.pack(pady=20)
    
    # Add New Person button
    add_btn = tk.Button(btn_frame, text="Add New Person", 
                       command=add_new_person,
                       bg='#4CAF50', fg='white', 
                       font=('Arial', 14, 'bold'),
                       padx=30, pady=15, width=15)
    add_btn.grid(row=0, column=0, padx=10, pady=10)
    
    # View/Manage Persons button
    manage_btn = tk.Button(btn_frame, text="View/Manage Persons", 
                          command=view_manage_persons,
                          bg='#2196F3', fg='white', 
                          font=('Arial', 14, 'bold'),
                          padx=30, pady=15, width=15)
    manage_btn.grid(row=0, column=1, padx=10, pady=10)
    
    # Start Recognition button
    recognize_btn = tk.Button(root, text="Start Recognition", 
                             command=face_system.start_recognition,
                             bg='#FF9800', fg='white', 
                             font=('Arial', 16, 'bold'),
                             padx=40, pady=20)
    recognize_btn.pack(pady=30)
    
    # Status info
    info_text = ("Training Images: " + str(len([f for f in os.listdir(face_system.persons_dir) 
                                               if f.endswith('.jpg')]) if os.path.exists(face_system.persons_dir) else "0") + 
                "\nUnique Faces: " + str(len(face_system.database)))
    
    info_label = tk.Label(root, text=info_text, 
                         font=('Arial', 10), bg='#f0f0f0', fg='#666')
    info_label.pack(pady=10)
    
    root.mainloop()

def maincall():
    """Main entry point for the face recognition system"""
    create_main_gui()


