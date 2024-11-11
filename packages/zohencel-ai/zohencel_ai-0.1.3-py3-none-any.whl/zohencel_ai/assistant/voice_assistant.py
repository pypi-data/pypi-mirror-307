# zohencel_ai/assistant/main.py
import os
import speech_recognition as sr
import pyttsx3
from .Grog_streaming import get_qadrix  # Adjust this to absolute if running standalone
import assemblyai as aai

# Get the API key from environment variables
aai.settings.api_key = "6ca0a16eb5e34f7ebf3db8204a55ff55"
recognizer = sr.Recognizer()
transcriber = aai.Transcriber()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180)

def speak(text, voice: str = 'male'):
    if voice.lower() == 'male':
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        text = recognizer.recognize_google(audio)
        print("Recognized text from speech recognition:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

messages = [
    {
        "role": "system",
        "content": "You're a helpful voice assistant. Make your sound funny and informative and also engaging to the user. Keep the response as short as possible."
    }
]

def run_voice_assistant(voice):
    global messages
    while True:
        text = listen()
        if text:
            if len(messages) > 5:
                messages = messages[:1] + messages[-4:]
            messages.append({"role": "user", "content": text})
            response = get_qadrix(messages)
            speak(response,voice)
            messages.append({"role": "assistant", "content": response})
