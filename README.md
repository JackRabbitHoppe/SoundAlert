# SoundAlert: Custom Audio Notifications for Deaf Users

## 🚧 Problem
Deaf and hard-of-hearing users miss out on critical real-world sounds like doorbells and fire alarms.

## 💡 Solution
A Python-based system that uses machine learning (YAMNet) to detect sounds and send custom alerts.

## 🔧 Features
- Sound classification with YAMNet
- Real-time popup alerts (Tkinter)
- Custom audio input (converted to 16kHz mono)

## How to run:
- python -m venv soundenv
- soundenv\Scripts\activate  # or source soundenv/bin/activate on macOS/Linux
- pip install -r requirements.txt

## 📦 Tips:
- python soundAI.py (change file parameter for different sounds)
- Need to ensure that sound is: MONO, 16khz, and .wav (I've used Freesound but there must be other places)
- Can use ffmpeg to convert audio and also trim
- ffmpeg (<-- path to the .exe file) -i Bell.wav -ss 00:00:01 -t 5 (time) -ac 1 -ar 16000 (16khz) Bell_trimmed_converted.wav

