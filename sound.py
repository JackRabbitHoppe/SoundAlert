# sound_alert_app.py
import tkinter as tk
#import sounddevice as sd
import numpy as np
#from playsound import playsound
import threading
from tkinter import messagebox
import pygame



def play_doorbell():
    # Simulate a doorbell sound
    playsound('doorbell.wav')  # make sure you have a sample sound file

def show_alert():
    alert = tk.Toplevel()
    alert.geometry("300x100")
    alert.title("Alert!")
    label = tk.Label(alert, text="Doorbell Detected!", font=("Arial", 18))
    label.pack(pady=20)
    alert.after(3000, alert.destroy)

def simulate_detection():
    # Just simulate a sound detection for now
    play_doorbell()
    show_alert()

def play_sound(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()


def show_popup():
    popup = tk.Toplevel()
    popup.title("Alert")
    popup.geometry("300x100")

    label = tk.Label(popup, text="Doorbell Detected!", font=("Arial", 14))
    label.pack(pady=20)

    popup.after(3000, popup.destroy)  # auto-close after 3 seconds

def show_message():
    messagebox.showinfo("Alert", "Doorbell Detected!")

# UI setup
root = tk.Tk()
root.geometry("1000x600")
root.title("Sound Alert App")

label = tk.Label(root, text="Simulated Sound Alert System", font=("Arial", 14))
label.pack(pady=20)

btn = tk.Button(root, text="Simulate Alert 1", width=20, command=lambda: threading.Thread(target=simulate_detection).start())
btn.pack(pady=20)

btn = tk.Button(root, text="Simulate Alert 2", width=20, command=show_popup)
btn.pack(pady=20)

btn = tk.Button(root, text="Simulate Alert 3", width=20, command=show_message)
btn.pack(pady=20)

root.mainloop()
