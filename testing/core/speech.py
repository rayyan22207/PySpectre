import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()

def speak(text):
    print(f"🗣️ AI: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"🧠 You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Network error.")
            return ""

# Main Loop
while True:
    command = listen()
    if not command:
        continue

    if "hello" in command:
        speak("Hey Rayyan, ready to take over the world?")
    elif "exit" in command:
        speak("Goodbye, boss.")
        break
    else:
        # Echo anything that's not a known command
        speak(f"You said: {command}")
