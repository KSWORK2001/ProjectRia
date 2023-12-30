import sys
import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import os
import geocoder
import requests

def recognize_speech(timeout=5, custom_energy_threshold=4000):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.energy_threshold = custom_energy_threshold
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

def generate_response(user_input, api_key):
    if any(phrase in user_input for phrase in ["goodbye", "bye", "see you"]):
        return "Seeya! Have a great day."
    elif "spotify" in user_input.lower():
        open_application("Spotify")
        return "Opening Spotify..."
    elif "chrome" in user_input.lower():
        open_application("Chrome")
        return "Opening Chrome..."
    elif "roblox" in user_input.lower():
        open_application("Roblox")
        return "Opening Roblox..."
    elif "how are you" in user_input.lower():
        return "I'm doing well, thank you!"
    elif "what's your name" in user_input.lower():
        return "I am Ria. I am created by my legendary brother."
    elif "weather" in user_input.lower():
        user_city, user_country, user_location = get_user_location()
        if user_city and user_country and user_location:
            weather_info = get_weather(user_location[0], user_location[1], api_key)
            return f"Current weather in {user_city}, {user_country}: {weather_info}"
        else:
            return "Could not determine user location."
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
        elif application_name == "Roblox":
            os.startfile("C:\\Users\\karan\\AppData\\Local\\Roblox\\Versions\\version-510663c9d33e4fd8\\RobloxPlayerBeta.exe")
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

def get_user_location():
    try:
        location = geocoder.ip('me')
        return location.city, location.country, location.latlng
    except Exception as e:
        return None, None, None

def get_weather(lat, lon, api_key):
    base_url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,hourly",
        "appid": api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            # Process and extract relevant weather information from 'data'
            # Note: 'data' may contain various weather details for the specified location
            # Extract the information you need based on your requirements.
            return "Weather details here"
        else:
            return f"Error: {data['message']}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Replace 'YOUR_OPENWEATHERMAP_API_KEY' with your actual OpenWeatherMap API key
    api_key = 'ALREADY PUT THE KEY'


    speak("Hey there! I'm Ria... How can I help you today?")
    
    exit_program = False
    
    while not exit_program:
        user_input = recognize_speech(timeout=5)
        if user_input:
            print("You said:", user_input)
            response = generate_response(user_input, api_key)
            print("Ria:", response)
            speak(response)

            if any(phrase in user_input for phrase in ["goodbye", "bye", "see you"]):
                exit_program = True
            elif "spotify" in user_input.lower():
                open_application("Spotify")
