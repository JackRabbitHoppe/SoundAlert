import tkinter as tk
from tkinter import messagebox, colorchooser
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap import ttk
import threading
import pygame
import os
import json
from datetime import datetime
from twilio.rest import Client

# Initialize themed style
style = Style("superhero")  # Try: superhero, flatly, lumen, solar, etc.
root = style.master
root.geometry("800x600")
root.title("\U0001F50A Sound Alert System")

# Sound event directory
SOUND_DIR = "SoundEvents"
CONFIG_FILE = "sound_alert_config.json"

# Twilio credentials (replace with your actual credentials)
TWILIO_SID = 'ACbc1f53b68e79aa90fb61e02070ab34af'
TWILIO_TOKEN = '0c49713f41c297e6592ecb1100324437'
TWILIO_FROM = '+18338639378'
TO_PHONE = '+12818380414'

# Default configurations
DEFAULT_EVENTS = [
    ("Option1_converted.wav", "Doorbell", {"bg": "#fff8dc", "size": "medium", "duration": 3000, "call": False}),
    ("gunshots2_x.wav", "Gunshots", {"bg": "#ffe4e1", "size": "large", "duration": 4000, "call": True}),
    ("ghost.wav", "Ghost", {"bg": "#e6e6fa", "size": "small", "duration": 3500, "call": False}),
    ("explosion_x.wav", "Explosion", {"bg": "#ffcccb", "size": "large", "duration": 5000, "call": True}),
    ("fart_z.wav", "Fart", {"bg": "#f0fff0", "size": "medium", "duration": 2500, "call": False}),
    ("baby_cry.wav", "Baby Cry", {"bg": "#e0ffff", "size": "medium", "duration": 4500, "call": True})
]

# Load or initialize sound events
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config_data = json.load(f)
    SOUND_EVENTS = [(item["file"], item["label"], item["config"]) for item in config_data]
else:
    SOUND_EVENTS = DEFAULT_EVENTS.copy()

# Size mapping
SIZE_MAP = {
    "small": "200x80",
    "medium": "600x400",
    "large": "1000x800"
}

# Initialize pygame mixer
pygame.mixer.init()

# Log entries
log_entries = []


def make_alert_call(sound_label):
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        call = client.calls.create(
            twiml=f'<Response><Say>Alert! {sound_label} detected.</Say></Response>',
            to=TO_PHONE,
            from_=TWILIO_FROM
        )
        print(f"Call initiated: {call.sid}")
    except Exception as e:
        print(f"Call failed: {e}")


def show_log_window():
    log_win = tk.Toplevel()
    log_win.geometry("300x400")
    log_win.title("Detection Log")
    ttk.Label(log_win, text="Detection Log", font=("Arial", 12, "bold")).pack(pady=5)
    log_listbox = tk.Listbox(log_win, font=("Arial", 10))
    log_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    for entry in log_entries:
        log_listbox.insert(tk.END, entry)
    log_listbox.yview_moveto(1)


def show_settings_window():
    settings = tk.Toplevel()
    settings.geometry("520x520")
    settings.title("Customize Alerts")

    canvas = tk.Canvas(settings)
    scrollbar = ttk.Scrollbar(settings, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def save_changes():
        global SOUND_EVENTS

        updated_events = []
        for i, (file, label, _) in enumerate(SOUND_EVENTS):
            updated_config = {
                "bg": color_vars[i].get(),
                "size": size_vars[i].get(),
                "call": call_vars[i].get()
            }
            try:
                updated_config["duration"] = int(duration_vars[i].get())
            except ValueError:
                updated_config["duration"] = 3000
            updated_events.append((file, label, updated_config))

        # Update global SOUND_EVENTS
        SOUND_EVENTS = updated_events

        # Save to JSON
        data = [
            {"file": file, "label": label, "config": config}
            for file, label, config in SOUND_EVENTS
        ]
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=2)

        # Re-render buttons
        for widget in button_frame.winfo_children():
            widget.destroy()

        ttk.Label(button_frame, text="\U0001F4E2 Sound Alert System", font=("Arial", 18, "bold")).pack(pady=10)
        for file, label, config in SOUND_EVENTS:
            ttk.Button(
                button_frame,
                text=f"▶ {label}",
                width=30,
                command=lambda f=file, l=label, c=config: trigger_event(f, l, c)
            ).pack(pady=5)

        settings.destroy()


    def reset_defaults():
        global SOUND_EVENTS
        SOUND_EVENTS = DEFAULT_EVENTS.copy()
        save_config()
        settings.destroy()

    def save_config():
        data = [
            {"file": file, "label": label, "config": config}
            for file, label, config in SOUND_EVENTS
        ]
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=2)

    color_vars = []
    size_vars = []
    duration_vars = []
    call_vars = []

    for i, (_, label, config) in enumerate(SOUND_EVENTS):
        frame = ttk.Labelframe(scroll_frame, text=label, padding=10)
        frame.pack(fill="x", padx=10, pady=5)

        color_var = tk.StringVar(value=config["bg"])
        size_var = tk.StringVar(value=config["size"])
        duration_var = tk.StringVar(value=str(config["duration"]))
        call_var = tk.BooleanVar(value=config.get("call", False))

        color_vars.append(color_var)
        size_vars.append(size_var)
        duration_vars.append(duration_var)
        call_vars.append(call_var)

        def choose_color(var=color_var):
            color = colorchooser.askcolor(title="Choose background color")[1]
            if color:
                var.set(color)

        ttk.Label(frame, text="Background:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=color_var, width=12).grid(row=0, column=1)
        ttk.Button(frame, text="Pick", command=choose_color).grid(row=0, column=2)

        ttk.Label(frame, text="Size:").grid(row=1, column=0, sticky="w")
        ttk.OptionMenu(frame, size_var, size_var.get(), "small", "medium", "large").grid(row=1, column=1)

        ttk.Label(frame, text="Duration (ms):").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame, textvariable=duration_var, width=10).grid(row=2, column=1)

        ttk.Checkbutton(frame, text="Call Phone", variable=call_var).grid(row=3, column=0, columnspan=2, sticky="w")

    btn_frame = ttk.Frame(settings)
    btn_frame.pack(pady=10)
    ttk.Button(btn_frame, text="Save", command=save_changes, bootstyle=SUCCESS).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Reset to Default", command=reset_defaults, bootstyle=WARNING).pack(side="left", padx=5)


def log_detection(label):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {label}"
    log_entries.append(entry)


def play_sound(file):
    try:
        full_path = os.path.join(SOUND_DIR, file)
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showerror("Playback Error", str(e))


def show_alert(label, config):
    bg_color = config.get("bg", "#ff0000")

    popup = tk.Toplevel(root)
    popup.geometry(SIZE_MAP.get(config["size"], "300x120"))
    popup.title("\u26A0 Alert!")
    popup.attributes("-topmost", True)

    canvas = tk.Canvas(popup, width=popup.winfo_width(), height=popup.winfo_height(), highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Wait until window actually renders to get correct dimensions
    popup.update_idletasks()
    width = popup.winfo_width()
    height = popup.winfo_height()

    # Draw a rectangle that fills the canvas
    canvas.create_rectangle(0, 0, width, height, fill=bg_color, outline=bg_color)

    # Draw the alert text
    canvas.create_text(
        width // 2, height // 2,
        text=f"Detected: {label}",
        fill="black",
        font=("Arial", 20, "bold")
    )

    popup.after(config["duration"], popup.destroy)


def trigger_event(file, label, config):
    def task():
        try:
            play_sound(file)
            show_alert(label, config)
            log_detection(label)
            if config.get("call"):
                make_alert_call(label)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    threading.Thread(target=task).start()


# Sound buttons frame
button_frame = ttk.Frame(root, padding=10)
button_frame.place(x=200, y=60)
ttk.Label(button_frame, text="\U0001F4E2 Sound Alert System", font=("Arial", 18, "bold")).pack(pady=10)

for file, label, config in SOUND_EVENTS:
    ttk.Button(
        button_frame,
        text=f"▶ {label}",
        width=30,
        command=lambda f=file, l=label, c=config: trigger_event(f, l, c)
    ).pack(pady=5)

# Top bar buttons
ttk.Button(root, text="View Log", width=15, bootstyle=INFO, command=show_log_window).place(x=20, y=20)
ttk.Button(root, text="Customize Alerts", width=18, bootstyle=PRIMARY, command=show_settings_window).place(x=640, y=20)

root.mainloop()
