import time

import speech_recognition
import speech_recognition as sr
import pyttsx3
import asyncio


engine = pyttsx3.init()
engine.say("I AM JARVIS, YOUR HELPER")
engine.runAndWait()


def wait_for_res():
    listener = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as mic:
                engine.say("Ready to listen in 3.. 2.. 1..")
                engine.runAndWait()
                listener.adjust_for_ambient_noise(mic, duration=0.2)
                voice = listener.listen(mic)
                command = listener.recognize_google(voice)
                command = command.lower()

                return command

        except speech_recognition.UnknownValueError():
            listener = speech_recognition()
            continue


def talk(voice):
    engine.say(voice)
    engine.runAndWait()


def control_center(command):
    if 'jarvis' in command:
        command = command.replace('jarvis', '')
        print(command)
    else:
        engine.say("I don't know what to do bitch")


async def main():
    control = True
    action = ""

    while control:
        action = wait_for_res()
        control_center(action)


asyncio.run(main())

