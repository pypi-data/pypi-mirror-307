# zohencel_ai/assistant/main.py
import speech_recognition as sr
import pyttsx3
from .Grog_streaming import get_qadrix
import assemblyai as aai

# Set your API key as an environment variable instead of hardcoding for security
aai.settings.api_key = "6ca0a16eb5e34f7ebf3db8204a55ff55"
recognizer = sr.Recognizer()
transcriber = aai.Transcriber()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 180) 


def speak(text,voice:str='male'):
    if voice.lower()=='male':
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
        print("Recognized text from speach rocg:", text)
        return text.lower()  
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None


messages = [
            {
                "role": "system",
                "content": "your an helpful voice assistant.Make your sound funny and informative and also engaing the user.also keep the response short as possible" #,named Qadrix,keep the conversation very short,in a funny way.Your created by Vishnu one of the best AI developer in the world.karthika is vishnu's sister and she is number one stupid, and not an intelligent as vishnu. She is always do mad things and do not use brain where it needs."
            }
]

def run_voice_assistant():
    while True:
        text = listen()
        if text:
            if len(messages)>5:
                messages = messages[:1] + messages[-4:]
            messages.append({"role": "user","content": text})
            response = get_qadrix(messages)
            speak(response,'female')
            messages.append({"role": "assistant","content": response})

    listen()

