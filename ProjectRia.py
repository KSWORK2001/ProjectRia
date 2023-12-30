import speech_recognition as sr
from gtts import gTTS
import pygame
import io

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)
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
    responses = {
        "hey ria": "Hey there, how can I help you today?",
        "how are you": "I'm doing well, thank you!",
        "what's your name": "I'm Ria! I am a virtual assistant desgned to help you tackle school!",
        "bye": "Goodbye! Have a great day.",
    }

    return responses.get(user_input.lower(), "I didn't understand that.")

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
    speak("Hello! I'm Ria. How can I help you today?")
    
    while True:
        user_input = recognize_speech()
        if user_input:
            print("You said:", user_input)
            response = generate_response(user_input)
            print("Assistant:", response)
            speak(response)
