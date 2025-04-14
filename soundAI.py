import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import soundfile as sf

# Load YAMNet model
print("Loading Model!")
model = hub.load('https://tfhub.dev/google/yamnet/1')

# Load a local audio file (must be mono, 16kHz WAV)
print("reading file")
waveform, sr = sf.read('Bell_converted.wav')
assert sr == 16000, "Audio must be 16 kHz"
print("Reading complete!")

# Run model
scores, embeddings, spectrogram = model(waveform)

# Get class names
class_map_path = model.class_map_path().numpy()
class_names = [line.strip() for line in tf.io.gfile.GFile(class_map_path)]

# Get top result
top_class = class_names[scores.numpy().mean(axis=0).argmax()]
print("Predicted:", top_class)
