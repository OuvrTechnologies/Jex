import psutil
import datetime
import time
import sounddevice as sd
import numpy as np

def get_cpu_percent():
    return psutil.cpu_percent(interval=1)

def get_memory_percent():
    return psutil.virtual_memory().percent

def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)

    print("\n")
    # Calculate sound level (RMS of the audio signal)
    volume_norm = np.linalg.norm(indata) * 10
    print("Time:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Sound Level: {:.2f} dB".format(volume_norm))
    print("CPU Percent: {:.2f}%".format(get_cpu_percent()))
    print("Memory Percent: {:.2f}%".format(get_memory_percent()))

    # Add other features or sensors here

    print("\n")

# Main loop for audio processing
channels = 1  # mono audio
samplerate = 44100  # audio sample rate
with sd.InputStream(callback=callback, channels=channels, samplerate=samplerate):
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\nInterrupted by user')
