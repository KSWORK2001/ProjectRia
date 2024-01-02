import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import os
import geocoder
import requests
import datetime

WAKE_WORD = "hey porcupine"  # Set your desired wake word
WAKE_WORD_THRESHOLD = 0.7

def recognize_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        wake_word = recognizer.recognize_google(audio).lower()
        print(f"Detected wake word: {wake_word}")
        return wake_word.startswith(WAKE_WORD)
    except sr.UnknownValueError:
        return False
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return False

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
        print(f"Could not request results; {e}")
        return None



def generate_response(user_input, api_key):
    if any(phrase in user_input for phrase in ["goodbye", "bye", "see you", "thank you", "thanks"]):
        return "Seeya! Have a great day."
    elif "spotify" in user_input.lower():
        open_application("Spotify")
        return "Opening Spotify..."
    elif "hey porcupine" in user_input.lower():
        return "Hey there, how can I be of service?"
    elif any(word in user_input.lower() for word in ["chrome", "browser"]):
        open_application("Chrome")
        return "Opening Chrome..."
    elif "roblox" in user_input.lower():
        open_application("Roblox")
        return "Opening Roblox..."
    elif any(word in user_input.lower() for word in ["mail", "email", "outlook"]):
        open_application("Outlook")
        return "Opening Outlook..."
    elif "how are you" in user_input.lower():
        return "I'm doing well, thank you!"
    elif "what's your name" in user_input.lower():
        return "I am a voice assistant designed for Atul Shrivastava."
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
        elif application_name == "Outlook":
            os.startfile("C:\\Program Files\\Microsoft Office\\Office16\\OUTLOOK.exe")
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
    base_url = "https://api.openweathermap.org/data/2.5/onecall"
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
            # Extract current weather information
            current_weather = data['current']
            
            # Extract current temperature
            current_temp = current_weather['temp']
            
            # Extract today's weather information
            today_weather = data['daily'][0]

            # Extract high and low temperatures for today
            high_temp = today_weather['temp']['max']
            low_temp = today_weather['temp']['min']

            # Convert temperatures from Kelvin to Celsius (or Fahrenheit if needed)
            current_temp_celsius = round(current_temp - 273.15, 2)
            high_temp_celsius = round(high_temp - 273.15, 2)
            low_temp_celsius = round(low_temp - 273.15, 2)

            # Display the weather details for today
            return f"Current Temperature: {current_temp_celsius} degree Celsius\nWeather for today: High {high_temp_celsius} degree Celsius, Low {low_temp_celsius} degree Celsius"
        else:
            return f"Error: {data['message']}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    api_key = 'KEY CONTENT HERE'

    current_time = datetime.datetime.now().hour
   
    if 6 <= current_time < 12:
        speak("Good Morning Atul, ready to help!")
    elif 12 <= current_time < 18:
        speak("Good Afternoon Atul, here to make your day!")
    else:
        speak("Good Evening Atul, here to help!") 

    exit_program = False
    
    while not exit_program:
        if recognize_wake_word():
            speak("How can I help?")
            user_input = recognize_speech(timeout=5)
            if user_input:
                print("You said:", user_input)
                response = generate_response(user_input, api_key)
                print("Porcupine:", response)
                speak(response)

                if any(phrase in user_input for phrase in ["goodbye", "bye", "see you"]):
                    exit_program = True
                elif "spotify" in user_input.lower():
                    open_application("Spotify")
                elif "chrome" in user_input.lower():
                    open_application("Chrome")
                elif "roblox" in user_input.lower():
                    open_application("Roblox")
                elif "outlook" in user_input.lower():
                    open_application("Outlook")