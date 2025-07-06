import speech_recognition as sr
import pyttsx3
import whisper
import sounddevice as sd
import numpy as np
import pvporcupine
import struct
import pyaudio
import datetime
import webbrowser
import os
from dotenv import load_dotenv
load_dotenv()
access_key = os.getenv("PORCUPINE_ACCESS_KEY")
print(access_key)


# Initialize
engine = pyttsx3.init()
engine.setProperty('rate', 170)
model = whisper.load_model("base")

# Speak
def speak(text):
    print(f"🗣️ Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# Record for Whisper fallback
def record_audio(duration=4, fs=16000):
    print("🎙️ Recording fallback...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    return np.squeeze(audio)

# Google STT
def recognize_google():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening (Google)...")
        audio = r.listen(source, timeout=5)
        try:
            text = r.recognize_google(audio)
            print(f"🧠 Google heard: {text}")
            return text.lower()
        except:
            return None

# Whisper fallback
def recognize_whisper():
    audio = record_audio()
    result = model.transcribe(audio)
    text = result["text"].strip().lower()
    print(f"🧠 Whisper heard: {text}")
    return text

# Process command
def process_command(text):
    if "hello" in text:
        speak("Hey Rayyan, I’m online and fully operational.")
    elif "exit" in text or "quit" in text:
        speak("Shutting down. See you later.")
        return False
    elif "time" in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"It is {now}")
    elif "open google" in text:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    elif "what can you do" in text:
        speak("I can listen, respond, and help you build the future.")
    else:
        speak(f"You said: {text}")
    return True

# Wake word using Porcupine
def listen_for_wake_word():
    porcupine = pvporcupine.create(access_key=access_key,keywords=["computer"])  # Replace with "jarvis" if custom keyword added
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )

    print("👂 Waiting for wake word...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)

            if porcupine.process(pcm_unpacked):
                speak("Yes?")
                text = recognize_google()
                if not text:
                    text = recognize_whisper()

                if text:
                    if not process_command(text):
                        break
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

# Start Jarvis
if __name__ == "__main__":
    listen_for_wake_word()
