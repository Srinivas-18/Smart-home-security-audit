import tkinter as tk
import tkinter.font as font
from in_out import in_out
from motion import noise
from rect_noise import rect_noise
from record import record
from PIL import Image, ImageTk
from find_motion import find_motion
from identify import maincall

import os
import platform
import subprocess
from tkinter import Toplevel, Label, Entry, Button, messagebox
from dotenv import load_dotenv

load_dotenv()  # Load credentials from .env file

def open_log():
    def authenticate():
        entered_user = user_entry.get()
        entered_pass = pass_entry.get()

        valid_user = os.getenv("LOG_USERNAME")
        valid_pass = os.getenv("LOG_PASSWORD")

        if entered_user == valid_user and entered_pass == valid_pass:
            login_win.destroy()
            log_file = "alert_log.csv"
            if not os.path.exists(log_file):
                messagebox.showerror("Error", "Log file not found.")
                return
            try:
                if platform.system() == "Windows":
                    os.startfile(log_file)
                elif platform.system() == "Darwin":
                    subprocess.call(["open", log_file])
                else:
                    subprocess.call(["xdg-open", log_file])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open log file: {e}")
        else:
            messagebox.showerror("Access Denied", "Invalid username or password.")

    login_win = Toplevel()
    login_win.title("Login")
    login_win.geometry("300x160")
    login_win.resizable(False, False)

    Label(login_win, text="Username:").pack(pady=(10, 2))
    user_entry = Entry(login_win, width=30)
    user_entry.pack()

    Label(login_win, text="Password:").pack(pady=(10, 2))
    pass_entry = Entry(login_win, show='*', width=30)
    pass_entry.pack()

    Button(login_win, text="Login", command=authenticate).pack(pady=10)

window = tk.Tk()
window.title("Smart Surveillance System")
window.iconphoto(False, tk.PhotoImage(file='mn.png'))
window.configure(bg='orange')
window.geometry('1080x700')

frame1 = tk.Frame(window)

label_title = tk.Label(frame1, text="Smart Surveillance System", fg='blue')
label_font = font.Font(size=35, weight='bold', family='Times New Roman')
label_title['font'] = label_font
label_title.grid(pady=(10,10), column=2)

icon = Image.open('icons/cc1.png')
icon = icon.resize((120, 120))
icon = ImageTk.PhotoImage(icon)
label_icon = tk.Label(frame1, image=icon)
label_icon.grid(row=1, pady=(5,10), column=2)

btn1_image = Image.open('icons/mon1.png').resize((40, 40))
btn1_image = ImageTk.PhotoImage(btn1_image)

btn2_image = Image.open('icons/rectangle-of-cutted-line-geometrical-shape.png').resize((30, 30))
btn2_image = ImageTk.PhotoImage(btn2_image)

btn3_image = Image.open('icons/noise1.png').resize((40, 40))
btn3_image = ImageTk.PhotoImage(btn3_image)

btn4_image = Image.open('icons/rec1.png').resize((40, 40))
btn4_image = ImageTk.PhotoImage(btn4_image)

btn5_image = Image.open('icons/exit.png').resize((40, 40))
btn5_image = ImageTk.PhotoImage(btn5_image)

btn6_image = Image.open('icons/incognito.png').resize((40, 40))
btn6_image = ImageTk.PhotoImage(btn6_image)

btn7_image = Image.open('icons/iden1.png').resize((40, 40))
btn7_image = ImageTk.PhotoImage(btn7_image)

btn8_image = Image.open('icons/log.png').resize((40, 40)) if os.path.exists('icons/log.png') else None
if btn8_image: btn8_image = ImageTk.PhotoImage(btn8_image)

btn_font = font.Font(size=18)
btn1 = tk.Button(frame1, text='Monitor', height=60, width=140, fg='blue', command=find_motion, image=btn1_image, compound='left')
btn1['font'] = btn_font
btn1.grid(row=3, pady=(25,10))

btn2 = tk.Button(frame1, text='Rectangle', height=60, width=140, fg='blue', command=rect_noise, image=btn2_image, compound='left')
btn2['font'] = btn_font
btn2.grid(row=3, pady=(20,10), column=3, padx=(20,5))

btn3 = tk.Button(frame1, text='Noise', height=60, width=140, fg='blue', command=noise, image=btn3_image, compound='left')
btn3['font'] = btn_font
btn3.grid(row=5, pady=(25,10))

btn4 = tk.Button(frame1, text='Record', height=60, width=140, fg='blue', command=record, image=btn4_image, compound='left')
btn4['font'] = btn_font
btn4.grid(row=5, pady=(20,10), column=3, padx=(20,10))

btn6 = tk.Button(frame1, text='In Out', height=60, width=140, fg='blue', command=in_out, image=btn6_image, compound='left')
btn6['font'] = btn_font
btn6.grid(row=5, pady=(20,10), column=2)

btn7 = tk.Button(frame1, text='Identify', height=60, width=140, fg='blue', command=maincall, image=btn7_image, compound='left')
btn7['font'] = btn_font
btn7.grid(row=3, column=2, pady=(20,10))

btn8 = tk.Button(frame1, text='View Log', height=60, width=140, fg='blue', command=open_log, image=btn8_image, compound='left' if btn8_image else None)
btn8['font'] = btn_font
btn8.grid(row=6, pady=(20,10), column=1)

btn5 = tk.Button(frame1, height=60, width=140, fg='blue', command=window.quit, image=btn5_image)
btn5['font'] = btn_font
btn5.grid(row=6, pady=(20,10), column=2)

frame1.pack()
window.mainloop()