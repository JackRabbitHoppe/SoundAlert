import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap import ttk
import threading
import pygame
import os
import json
from datetime import datetime
from twilio.rest import Client

style = Style("superhero")
root = style.master
root.state('zoomed')
root.title("\U0001F50A Sound Alert System")

SOUND_DIR = "SoundEvents"
CONFIG_FILE = "sound_alert_config.json"

TWILIO_SID = ''
TWILIO_TOKEN = ''
TWILIO_FROM = '+18338639378'
TO_PHONE_VAR = tk.StringVar(value="2818380414")

DEFAULT_EVENTS = [
    ("Option1_converted.wav", "Doorbell", {"bg": "#fff8dc", "size": "medium", "duration": 3000, "call": False}),
    ("gunshots2_x.wav", "Gunshots", {"bg": "#ffe4e1", "size": "large", "duration": 4000, "call": True}),
    ("ghost.wav", "Ghost", {"bg": "#e6e6fa", "size": "small", "duration": 3500, "call": False}),
    ("explosion_x.wav", "Explosion", {"bg": "#ffcccb", "size": "large", "duration": 5000, "call": True}),
    ("fart_z.wav", "Fart", {"bg": "#f0fff0", "size": "medium", "duration": 2500, "call": False}),
    ("baby_cry.wav", "Baby Cry", {"bg": "#e0ffff", "size": "medium", "duration": 4500, "call": True})
]

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config_data = json.load(f)
    SOUND_EVENTS = [(item["file"], item["label"], item["config"]) for item in config_data]
else:
    SOUND_EVENTS = DEFAULT_EVENTS.copy()

SIZE_MAP = {
    "small": "200x80",
    "medium": "600x400",
    "large": "1000x800"
}

COLOR_PRESETS = [
    ("Red", "#ff4c4c"),
    ("Green", "#4caf50"),
    ("Blue", "#2196f3"),
    ("Yellow", "#ffeb3b"),
    ("Cyan", "#00bcd4"),
    ("Magenta", "#e91e63"),
    ("Orange", "#ff9800"),
    ("Purple", "#9c27b0"),
    ("Gray", "#9e9e9e")
]

pygame.mixer.init()
log_entries = []


def make_alert_call(sound_label):
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        full_number = f"+1{TO_PHONE_VAR.get()}"
        call = client.calls.create(
            twiml=f'<Response><Say>Alert! {sound_label} detected.</Say></Response>',
            to=full_number,
            from_=TWILIO_FROM
        )
        print(f"Call initiated: {call.sid}")
    except Exception as e:
        print(f"Call failed: {e}")


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


def fade_in(window, step=0.05):
    alpha = 0.0
    window.attributes('-alpha', alpha)
    def _fade():
        nonlocal alpha
        alpha += step
        if alpha <= 1.0:
            window.attributes('-alpha', alpha)
            window.after(30, _fade)
    _fade()


def show_alert(label, config):
    bg_color = config.get("bg", "#ff0000")

    popup = tk.Toplevel(root)
    popup.geometry(SIZE_MAP.get(config["size"], "300x120"))
    popup.title("\u26A0 Alert!")
    popup.attributes("-topmost", True)

    fade_in(popup)

    canvas = tk.Canvas(popup, width=popup.winfo_width(), height=popup.winfo_height(), highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    popup.update_idletasks()
    width = popup.winfo_width()
    height = popup.winfo_height()

    canvas.create_rectangle(0, 0, width, height, fill=bg_color, outline=bg_color)
    canvas.create_text(width // 2, height // 2, text=f"Detected: {label}", fill="black", font=("Arial", 20, "bold"))

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


def show_log_window():
    log_win = tk.Toplevel(root)
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
    settings.geometry("600x600")
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

        SOUND_EVENTS = updated_events

        data = [
            {"file": file, "label": label, "config": config}
            for file, label, config in SOUND_EVENTS
        ]
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=2)

        for widget in center_frame.winfo_children():
            widget.destroy()

        ttk.Label(center_frame, text="\U0001F4E2 Sound Alert System", font=("Arial", 24, "bold")).pack(pady=(0, 20))
        ttk.Label(center_frame, text="Trigger Sound Events", font=("Arial", 16)).pack()
        for file, label, config in SOUND_EVENTS:
            ttk.Button(
                center_frame,
                text=f"▶ {label}",
                width=30,
                command=lambda f=file, l=label, c=config: trigger_event(f, l, c)
            ).pack(pady=5)

        control_frame = ttk.Frame(center_frame, padding=10)
        control_frame.pack(pady=(20, 0))
        ttk.Button(control_frame, text="View Log", width=18, bootstyle=INFO, command=show_log_window).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Customize Alerts", width=18, bootstyle=PRIMARY, command=show_settings_window).pack(side="left", padx=5)
        ttk.Label(control_frame, text="Phone to Call:").pack(side="left", padx=5)
        ttk.Entry(control_frame, textvariable=TO_PHONE_VAR, width=15).pack(side="left")

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

        ttk.Label(frame, text="Background:").grid(row=0, column=0, sticky="w")

        preview = tk.Label(frame, width=3, background=color_var.get(), relief="solid")
        preview.grid(row=0, column=2, padx=(5, 0))

        def update_color_preview(var=color_var, widget=preview):
            widget.configure(bg=var.get())

        color_var.trace_add("write", lambda *_: update_color_preview())

        preset_menu = ttk.OptionMenu(
            frame,
            color_var,
            color_var.get(),
            *[label for label, hexcode in COLOR_PRESETS],
            command=lambda selected_label, var=color_var, widget=preview: (var.set(dict(COLOR_PRESETS)[selected_label]), widget.configure(bg=dict(COLOR_PRESETS)[selected_label]))
        )
        preset_menu.grid(row=0, column=1, sticky="w")

        ttk.Label(frame, text="Size:").grid(row=1, column=0, sticky="w")
        ttk.OptionMenu(frame, size_var, size_var.get(), "small", "medium", "large").grid(row=1, column=1)

        ttk.Label(frame, text="Duration (ms):").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame, textvariable=duration_var, width=10).grid(row=2, column=1)

        ttk.Checkbutton(frame, text="Call Phone", variable=call_var).grid(row=3, column=0, columnspan=2, sticky="w")

    btn_frame = ttk.Frame(settings)
    btn_frame.pack(pady=10)
    ttk.Button(btn_frame, text="Save", command=save_changes, bootstyle=SUCCESS).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Reset to Default", command=reset_defaults, bootstyle=WARNING).pack(side="left", padx=5)

# Centered frame for content
center_frame = ttk.Frame(root, padding=20)
center_frame.place(relx=0.5, rely=0.5, anchor="center")

# Header
ttk.Label(center_frame, text="\U0001F4E2 Sound Alert System", font=("Arial", 24, "bold")).pack(pady=(0, 20))

# Buttons
ttk.Label(center_frame, text="Trigger Sound Events", font=("Arial", 16)).pack()
for file, label, config in SOUND_EVENTS:
    ttk.Button(
        center_frame,
        text=f"▶ {label}",
        width=30,
        command=lambda f=file, l=label, c=config: trigger_event(f, l, c)
    ).pack(pady=5)

# Bottom controls
control_frame = ttk.Frame(center_frame, padding=10)
control_frame.pack(pady=(20, 0))

# Log and Customize
ttk.Button(control_frame, text="View Log", width=18, bootstyle=INFO, command=show_log_window).pack(side="left", padx=5)
ttk.Button(control_frame, text="Customize Alerts", width=18, bootstyle=PRIMARY, command=show_settings_window).pack(side="left", padx=5)

# Phone entry
ttk.Label(control_frame, text="Phone to Call:").pack(side="left", padx=5)
ttk.Entry(control_frame, textvariable=TO_PHONE_VAR, width=15).pack(side="left")

root.mainloop()


