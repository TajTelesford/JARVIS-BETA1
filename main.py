import speech_recognition as sr
import pyttsx3
from utils import *
from Jarvis import intents, predict_class, get_response

BACKGROUND_TASKS = set()
JARVIS_INTENTS = intents
engine = pyttsx3.init()
engine.say("I AM JARVIS, YOUR HELPER")
engine.runAndWait()


def wait_for_res():
    listener = sr.Recognizer()

    try:
        with sr.Microphone() as mic:
            engine.say("Ready")
            engine.runAndWait()
            voice = listener.listen(mic)
            command = listener.recognize_google(voice)
            command = command.lower()

            return command

    except:
        return None


def talk(voice):
    engine.say(voice)
    engine.runAndWait()


def control_center(command):
    jarvis_res_list = predict_class(command)
    JARVIS_WORDS = get_response(jarvis_res_list, JARVIS_INTENTS)
    if JARVIS_WORDS.lower() == 'stocks':
        talk(JARVIS_WORDS)
        get_stocks()
    talk(JARVIS_WORDS)


async def main():
    control = True
    count = 0

    while control:
        print(count)
        action = wait_for_res()
        if action is None:
            continue
        control_center(action)
        count += 1


asyncio.run(main())
