import speech_recognition as sr
import pyttsx3
from utils import *

BACKGROUND_TASKS = set()

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
            print(command)

            return command

    except:
        return None


def talk(voice):
    engine.say(voice)
    engine.runAndWait()


def control_center(command):
    if 'jarvis' in command:
        print("command heard")
        if 'stocks' in command:
            talk("Getting Stocks, give me a second to fetch data...")
            get_stocks()
            talk("Stocks are ready for you sir")

        if 'hello' in command:
            talk("Hello Taj")
    elif "" in command:
        talk("Say Something Please")

    else:
        engine.say("I don't know what to do bitch")


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
