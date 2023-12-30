import sys
import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import os

def recognize_speech(timeout=3):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=timeout)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {0}".format(e))
        return None

def generate_response(user_input):
    if any(phrase in user_input for phrase in ["goodbye", "bye", "see you"]):
        return "See Ya! Have a great day."
    elif "open spotify" in user_input.lower():
        open_application("Spotify")
        return "Opening Spotify..."
    elif "open chrome" in user_input.lower():
        open_application("Chrome")
        return "Opening Chrome..."
    elif "how are you" in user_input.lower():
        return "I'm doing well, thank you!"
    elif "what's your name" in user_input.lower():
        return "I'm a virtual assistant. You can call me Ria."
    elif "bye" in user_input.lower():
        return "Goodbye! Have a great day."
    else:
        return "I didn't understand that."

def open_application(application_name):
    try:
        if application_name == "Spotify":
            os.startfile("C:\\Users\\karan\\AppData\\Roaming\\Spotify\\Spotify.exe")
        elif application_name == "Chrome":
            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    except Exception as e:
        print(f"Error opening {application_name}: {e}")

def speak(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    
    # Convert gTTS response to an audio file-like object
    audio_file = io.BytesIO()
    tts.write_to_fp(audio_file)
    
    # Play the audio using pygame
    audio_file.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

if __name__ == "__main__":
    speak("Hey there! I'm Ria... How can I help you today?")
    
    exit_program = False
    
    while not exit_program:
        user_input = recognize_speech(timeout=2)
        if user_input:
            print("You said:", user_input)
            response = generate_response(user_input)
            print("Ria:", response)
            speak(response)

            if any(phrase in user_input for phrase in ["goodbye", "bye", "see you"]):
                exit_program = True
            elif "open spotify" in user_input.lower():
                open_application("Spotify")
            elif "open chrome" in user_input.lower():
                open_application("Chrome")
