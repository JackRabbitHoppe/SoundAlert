import soundfile as sf

waveform, sr = sf.read('Option1_converted.wav')

# Sample rate
print("Sample Rate:", sr)

# Channels
if len(waveform.shape) == 1:
    print("Audio is MONO")
elif len(waveform.shape) == 2:
    print(f"Audio is STEREO with {waveform.shape[1]} channels")
else:
    print("Unexpected audio format")

# Duration (optional)
duration = len(waveform) / sr
print(f"Duration: {duration:.2f} seconds")
