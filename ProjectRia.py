import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import subprocess

"""def recognize_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        wake_word = recognizer.recognize_google(audio).lower()
        return "hey ria" in wake_word
    except sr.UnknownValueError:
        return False
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return False"""

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
        print("Could not request results; {0}".format(e))
        return None

def generate_response(user_input):
    if "open spotify" in user_input.lower():
        open_spotify()
        return "Opening Spotify..."
    elif "how are you" in user_input.lower():
        return "I'm doing well, thank you!"
    elif "what's your name" in user_input.lower():
        return "I'm a virtual assistant. You can call me Ria."
    elif "bye" in user_input.lower():
        return "Goodbye! Have a great day."
    else:
        return "I didn't understand that."

def open_spotify():
    try:
        subprocess.Popen(["C:\\Users\\karan\\AppData\\Roaming\\Spotify\\Spotify.exe"])
    except Exception as e:
        print(f"Error opening Spotify: {e}")

def speak(text):
    tts = gTTS(text=text, lang='en')
    
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
    
    while True:
        #if recognize_wake_word():                                              #Work on Recognizing Wake Word
        if True:
            user_input = recognize_speech(timeout=5)
            if user_input:
                print("You said:", user_input)
                response = generate_response(user_input)
                print("Ria:", response)
                speak(response)
