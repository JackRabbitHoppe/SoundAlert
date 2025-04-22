import tkinter as tk
from tkinter import messagebox
import threading
import pygame

# Sounds events and lables
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
root.geometry("600x500")
root.title("Sound Alert System")


def play_sound(file):
    try:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showerror("Playback Error", str(e))


def show_alert(label):
    popup = tk.Toplevel()
    popup.geometry("300x100")
    popup.title("Alert!")
    msg = f"Detected: {label}"
    tk.Label(popup, text=msg, font=("Arial", 14)).pack(pady=20)
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
tk.Label(root, text="Trigger Sound Alerts", font=("Arial", 12)).pack(pady=20)

for file, label in SOUND_EVENTS:
    tk.Button(root, text=f"Simulate: {label}", width=30, command=lambda f=file, l=label: trigger_event(f, l)).pack(pady=5)

root.mainloop()
