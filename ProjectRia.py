import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import os
import geocoder
import requests
import datetime
import webbrowser
from dateutil import parser
import time

WAKE_WORDS = ["hey porcupine", "play porcupine"]
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
        return any(wake_word.startswith(word) for word in WAKE_WORDS)
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
    if any(phrase in user_input for phrase in ["goodbye", "bye", "see you"]):
        return "Seeya! Have a great day."
    elif "spotify" in user_input.lower():
        open_application("Spotify")
        return "Opening Spotify..."
    elif any(word in user_input.lower() for word in ["chrome", "browser"]):
        open_application("Chrome")
        return "Opening Chrome..."
    elif "open google" in user_input.lower():
        open_application("Chrome", link="https://www.google.com/")
        return "Google is here"
    elif "open nexcen" in user_input.lower():
        open_application("Chrome", link="https://www.nexcenglobal.com/")
        return "Nexcen's Page is here"
    elif "open gmail" in user_input.lower():
        open_application("Chrome", link="https://mail.google.com/mail/u/0/#inbox")
        return "Gmail's open"
    elif "open drive" in user_input.lower():
        open_application("Chrome", link="https://drive.google.com/drive/u/0/my-drive")
        return "Drive's open"
    elif "roblox" in user_input.lower():
        open_application("Roblox")
        return "Opening Roblox..."
    elif any(word in user_input.lower() for word in ["mail", "email", "outlook"]):
        open_application("Outlook")
        return "Opening Outlook..."
    elif "how are you" in user_input.lower():
        return "I'm doing well, thank you!"
    elif "remind me to" in user_input.lower():
        try:
            reminder_text = user_input.lower().replace("remind me to", "").strip()
            parsed_datetime = parser.parse(reminder_text, fuzzy_with_tokens=True)

            # Check if a valid future date and time were parsed
            if parsed_datetime[0] and parsed_datetime[0] > datetime.datetime.now():
                reminder_text = f"Reminder: {reminder_text} - {parsed_datetime[0].strftime('%Y-%m-%d %H:%M:%S')}"
                response = add_reminder(reminder_text, reminders_file)
            else:
                response = "Invalid date or time. Please provide a future date and time for the reminder."

        except ValueError:
            response = "Invalid date or time format. Please provide a valid date and time for the reminder."

        return response
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
    
def add_reminder(reminder, file_path='reminders.txt'):
    try:
        with open(file_path, 'a') as file:
            file.write(reminder + '\n')
        print("Reminder added successfully.")
    except Exception as e:
        print(f"Error adding reminder: {e}")

def read_reminders(file_path='reminders.txt'):
    reminders = []
    try:
        with open(file_path, 'r') as file:
            reminders = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"File '{file_path}' not found. No reminders loaded.")
    return reminders


def print_reminders(reminders):
    if not reminders:
        print("No reminders.")
    else:
        print("Reminders:")
        for reminder in reminders:
            print(reminder)

def open_application(application_name, link=None):
    try:
        if application_name == "Spotify":
            os.startfile("C:\\Users\\karan\\AppData\\Roaming\\Spotify\\Spotify.exe")
        elif application_name == "Chrome":
            os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        elif application_name == "Roblox":
            os.startfile("C:\\Users\\karan\\AppData\\Local\\Roblox\\Versions\\version-510663c9d33e4fd8\\RobloxPlayerBeta.exe")
        elif application_name == "Outlook":
            os.startfile("outlook.exe")  # Adjust this based on the actual Outlook executable
        elif link:
            webbrowser.open(link, new=2)  # Open link in default web browser
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
    
def check_upcoming_reminders(reminders, minutes_before=15):
    current_time = datetime.datetime.now()

    for reminder in reminders:
        # Extract the scheduled time from the reminder text
        scheduled_time_str = reminder.split('-')[-1].strip()
        
        try:
            scheduled_time = datetime.datetime.strptime(scheduled_time_str, '%Y-%m-%d %H:%M:%S')
            time_difference = scheduled_time - current_time
            
            # Check if the reminder is scheduled within the next 'minutes_before' minutes
            if 0 <= time_difference.total_seconds() <= minutes_before * 60:
                speak(f"Upcoming reminder: {reminder}")
        except ValueError:
            print(f"Invalid date/time format in reminder: {reminder}")

if __name__ == "__main__":
    api_key = 'c39e52218b15fbde02bc0d6cce878e1e'
    reminders_file = 'reminders.txt'
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
                if "read my reminders" in user_input.lower():
                    reminders = read_reminders(reminders_file)
                    speak("Here are your reminders:")
                    for reminder in reminders:
                        speak(reminder)
                    continue  # Continue to the next iteration of the loop
                
                response = generate_response(user_input, api_key)
                print("Porcupine:", response)

                # Check if the response is not empty before trying to speak
                if response:
                    speak(response)
                
                check_upcoming_reminders(reminders)

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
                elif "open google" in user_input.lower():
                    open_application("Chrome", link="https://www.google.com/")
                elif "open nexcen" in user_input.lower():
                    open_application("Chrome", link="https://www.nexcenglobal.com/")
                elif "open gmail" in user_input.lower():
                    open_application("Chrome", link="https://mail.google.com/mail/u/0/#inbox")    
                elif "open drive" in user_input.lower():
                    open_application("Chrome", link="https://drive.google.com/drive/u/0/my-drive")
                  