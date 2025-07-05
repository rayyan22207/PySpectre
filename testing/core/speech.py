import speech_recognition as sr
import pyttsx3
import whisper
import sounddevice as sd
import numpy as np
import datetime
import webbrowser

# Init
engine = pyttsx3.init()
engine.setProperty('rate', 170)
model = whisper.load_model("base")  # base is fast + accurate

def speak(text):
    print(f"🗣️ Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# Record audio for Whisper fallback
def record_audio(duration=4, fs=16000):
    print("🎤 Recording fallback...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    return np.squeeze(audio)

# Try Google STT
def recognize_google():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening (Google)...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"🧠 Google heard: {text}")
            return text.lower()
        except (sr.UnknownValueError, sr.RequestError):
            return None

# Fallback: Whisper STT
def recognize_whisper():
    audio = record_audio()
    result = model.transcribe(audio)
    text = result["text"].strip().lower()
    print(f"🧠 Whisper heard: {text}")
    return text

# Process voice command
def process_command(text):
    if "hello" in text:
        speak("Hey Rayyan, I’m online and watching everything.")
    elif "exit" in text or "quit" in text:
        speak("Shutting down, boss.")
        return False
    elif "time" in text:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
    elif "open google" in text:
        webbrowser.open("https://www.google.com")
        speak("Opening Google now.")
    elif "what can you do" in text:
        speak("I can control your system, search the web, and more. Just give me time.")
    else:
        speak(f"You said: {text}")
    return True

# Main loop
def main():
    while True:
        text = recognize_google()
        if not text:
            text = recognize_whisper()

        if text:
            if not process_command(text):
                break

if __name__ == "__main__":
    main()
