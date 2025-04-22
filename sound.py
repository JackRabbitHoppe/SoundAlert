import tkinter as tk
from tkinter import messagebox
import threading
import pygame
import os

# Sound event directory
SOUND_DIR = "SoundEvents"

# Hardcoded sound events and their labels
SOUND_EVENTS = [
    ("Option1_converted.wav", "Doorbell"),
    ("gunshots2_x.wav", "Gunshots"),
    ("ghost.wav", "Ghost"),
    ("explosion_x.wav", "Explosion"),
    ("fart_z.wav", "Fart"),
    ("baby_cry.wav", "Baby Cry")
]

# Initialize pygame mixer
pygame.mixer.init()

# GUI Setup
root = tk.Tk()
root.geometry("700x550")
root.title("\U0001F50A Sound Alert System")
root.configure(bg="#f0f4ff")


def play_sound(file):
    try:
        full_path = os.path.join(SOUND_DIR, file)
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showerror("Playback Error", str(e))


def show_alert(label):
    popup = tk.Toplevel(bg="#fff8dc")
    popup.geometry("300x120")
    popup.title("\u26A0 Alert!")
    msg = f"Detected: {label}"
    tk.Label(popup, text=msg, font=("Arial", 16), bg="#fff8dc").pack(pady=30)
    popup.after(3000, popup.destroy)


def trigger_event(file, label):
    def task():
        try:
            play_sound(file)
            show_alert(label)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    threading.Thread(target=task).start()


# GUI Elements
tk.Label(root, text="\U0001F4E2 Simulated Sound Alerts", font=("Arial", 18, "bold"), bg="#f0f4ff").pack(pady=30)

for file, label in SOUND_EVENTS:
    tk.Button(
        root,
        text=f"▶ {label}",
        width=30,
        font=("Arial", 12),
        bg="#dbeafe",
        activebackground="#93c5fd",
        command=lambda f=file, l=label: trigger_event(f, l)
    ).pack(pady=8)

root.mainloop()