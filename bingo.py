import pyttsx3
import speech_recognition as sr
import pyaudio
import os
from datetime import datetime, timedelta
import cv2
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
from requests import get
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
import pywhatkit as kit
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import time
import pyjokes
import subprocess
import pyautogui
import requests
import random
import smtplib
import tkinter as tk
from tkinter import filedialog
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Access the sensitive data from environment variables
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

file_path = './contact.csv'
contacts = pd.read_csv(file_path, sep=';', on_bad_lines='skip', engine='python')
contacts_filtered = contacts[['Name', 'Contact']]
contacts_filtered = contacts_filtered.dropna(subset=['Name', 'Contact'])
contact_dict = pd.Series(contacts_filtered['Contact'].values, index=contacts_filtered['Name'].str.lower()).to_dict()

engine = pyttsx3.init('nsss')
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voices', voices[0].id)

#text to audio
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# voice to text
def takecommand():
    try:
        recognizer = sr.Recognizer()
        os.system("osascript -e 'set volume input volume 100'")
        with sr.Microphone(device_index=0) as source:
            print("Adjusting for ambient noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = recognizer.listen(source, phrase_time_limit=5)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query

        except sr.UnknownValueError:
            print("Could not understand the audio. Please speak clearly.")
            return "none"
        except sr.RequestError as e:
            print(f"Recognition request failed; {e}")
            return "none"

    except Exception as e:
        print(f"An error occurred: {e}")
        return "none"


def wish():
    now = datetime.now()
    hour = now.hour
    minute = now.minute

    if 0 <= hour < 12:
        speak("Good morning!")
        speak(f"The time is {hour}:{minute:02d} AM.")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
        speak(f"The time is {hour - 12 if hour > 12 else hour}:{minute:02d} PM.")
    else:
        speak("Good evening!")
        speak(f"The time is {hour - 12 if hour > 12 else hour}:{minute:02d} PM.")

    speak("I am Bingo, here to assist you. How can I help you today?")

def open_spotify_web_with_track(track_uri):
    track_id = track_uri.split(":")[-1]
    web_url = f"https://open.spotify.com/track/{track_id}"
    try:
        webbrowser.open(web_url)
    except Exception as e:
        print(f"Could not open Spotify Web Player: {e}")

def play_random_song():
    # Search for a popular playlist and play a random track from it
    results = sp.search(q='Top Hits', type='playlist', limit=1)
    if results['playlists']['items']:
        playlist_uri = results['playlists']['items'][0]['uri']
        playlist_id = playlist_uri.split(":")[-1]
        tracks = sp.playlist_tracks(playlist_id)['items']

        if tracks:
            random_track = random.choice(tracks)
            track_uri = random_track['track']['uri']
            print(f"Playing {random_track['track']['name']} by {random_track['track']['artists'][0]['name']}...")
            open_spotify_web_with_track(track_uri)
            print("Please ensure you are logged into Spotify Web Player and press play.")
        else:
            print("No tracks found in the playlist.")
    else:
        print("Playlist not found. Please try again.")


SPOTIPY_REDIRECT_URI = 'http://localhost:8898/callback'
scope = 'user-read-playback-state'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
))

def open_spotify_web_with_track(track_uri):
    track_id = track_uri.split(":")[-1]
    web_url = f"https://open.spotify.com/track/{track_id}"
    try:
        webbrowser.open(web_url)
    except Exception as e:
        print(f"Could not open Spotify Web Player: {e}")

def play_random_song():
    # Search for a popular playlist and play a random track from it
    results = sp.search(q='Top Hits', type='playlist', limit=1)
    if results['playlists']['items']:
        playlist_uri = results['playlists']['items'][0]['uri']
        playlist_id = playlist_uri.split(":")[-1]
        tracks = sp.playlist_tracks(playlist_id)['items']

        if tracks:
            random_track = random.choice(tracks)
            track_uri = random_track['track']['uri']
            print(f"Playing {random_track['track']['name']} by {random_track['track']['artists'][0]['name']}...")
            open_spotify_web_with_track(track_uri)
            print("Please ensure you are logged into Spotify Web Player and press play.")
        else:
            print("No tracks found in the playlist.")
    else:
        print("Playlist not found. Please try again.")
def format_phone_number(phone_number):
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number
    return phone_number


def play_random_song_on_youtube(search_query="Top hits songs 2024"):
    video_url = kit.playonyt(search_query, open_video=False)
    if video_url:
        autoplay_url = video_url + "&autoplay=1"
        webbrowser.open(autoplay_url)
    else:
        print("Could not find a video to play.")

def fetch_news():
    url = f"https://newsapi.org/v2/everything?q=India&language=en&apiKey=={NEWS_API_KEY}"
    response = requests.get(url)
    news_data = response.json()

    if news_data["status"] == "ok" and news_data["totalResults"] > 0:
        articles = news_data["articles"]  # Get all articles
        headlines = [article["title"] for article in articles]
        return headlines
    else:
        return ["No news articles found at the moment."]


if __name__ == "__main__":
    wish()
    while True:
        query = takecommand().lower()

        if "open calculator" in query:
            npath = "/System/Applications/Calculator.app"
            os.system(f"open {npath}")
            print("Calculator is opening...")

        elif "open apple music" in query:
            npath = "/System/Applications/Music.app"
            os.system(f"open {npath}")
            print("Apple Music is opening...")

        elif "open firefox" in query:
            npath = "/System/Applications/Firefox.app"
            os.system(f"open {npath}")
            print("Firefox is opening...")

        elif "open numbers" in query:
            npath = "/Applications/Numbers.app"
            os.system(f"open {npath}")
            print("Numbers is opening...")

        elif "open photo booth" in query:
            npath = "/System/Applications/Photo Booth.app"
            os.system(f"open {npath}")
            print("photo booth is opening...")



        elif "open whatsapp" in query:
            npath = "/Applications/WhatsApp.app"
            os.system(f"open {npath}")
            print("whatsapp is opening...")

        elif "close whatsapp" in query:
            speak("closing whatsapp")
            os.system("pkill WhatsApp")



        elif "open xcode" in query:
            npath = "/Applications/Xcode.app"
            os.system(f"open {npath}")
            print("xcode is opening...")

        elif "open terminal" in query:
            os.system("open -a Terminal")
            print("Terminal is opening...")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k == 27:
                    break;
                cap.release()
                cap.destroyAllWindows()

        elif "close calculator" in query:
            speak("Closing Calculator")
            os.system("pkill Calculator")

        elif "close apple music" in query:
            speak("Closing Apple Music")
            os.system("pkill Music")

        elif "close firefox" in query:
            speak("Closing Firefox")
            os.system("pkill Firefox")

        elif "close numbers" in query:
            speak("Closing Numbers")
            os.system("pkill Numbers")

        elif "close photo booth" in query:
            speak("Closing Photo Booth")
            os.system("pkill 'Photo Booth'")

        elif "close xcode" in query:
            speak("Closing Xcode")
            os.system("pkill Xcode")

        elif "close terminal" in query:
            speak("Closing Terminal")
            os.system("pkill Terminal")

        elif "close camera" in query:
            speak("Closing Camera")
            os.system("pkill webcam")



        elif "play" in query:
            song = query.replace("play", "").replace("music", "").strip()
            if song:
                print(f"Playing {song} on Spotify...")
                results = sp.search(q=song, type='track', limit=1)

                if results['tracks']['items']:
                    track_uri = results['tracks']['items'][0]['uri']
                    print(
                        f"Found: {results['tracks']['items'][0]['name']} by {results['tracks']['items'][0]['artists'][0]['name']}")
                    print("Opening the song in Spotify Web Player...")
                    open_spotify_web_with_track(track_uri)
                    print("Please ensure you are logged into Spotify Web Player and press play.")
                else:
                    print("Song not found. Please try again.")
            else:

                print("Playing random music on Spotify...")
                play_random_song()

        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"your ip address is {ip}")
            print(f"your ip address is {ip}")

        elif "wikipedia" in query:
            try:
                speak("searching wikipedia ...")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("according to wikipedia")
                speak(results)
                print(results)
            except DisambiguationError as e:
                speak("The search term is ambiguous. Please be more specific.")
                print("Disambiguation error:", e.options)
            except PageError:
                speak("Sorry, no page was found for that search term.")

        elif "youtube" in query:
            if "search" in query:
                search_term = query.replace("youtube", "").replace("search", "").strip()
                if search_term:
                    search_term = search_term.replace(" ", "+")

                    webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")
                else:
                    speak("What would you like to search on YouTube?")
            else:

                webbrowser.open("https://www.youtube.com")

        elif "search" in query:

            search_term = query.replace("search", "").strip()
            if search_term:
                # Open Google search for the specified term
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
                speak(f"Searching for {search_term} on Google")
            else:
                speak("Please specify what you want to search for.")




        elif "send message" in query:
            speak("Would you like to send the message to a person or a number?")
            recipient_type = takecommand().lower()

            phone_number = None

            if "person" in recipient_type:
                speak("Whom would you like to send the message to?")
                contact_name = takecommand().lower()

                if contact_name in contact_dict:
                    phone_number = format_phone_number(contact_dict[contact_name])
                else:
                    speak("Sorry, I couldn't find that contact.")

            elif "number" in recipient_type:
                speak("Please provide the number.")
                phone_number = takecommand().lower()

                if not phone_number.startswith("+"):
                    speak("Please provide a valid international phone number starting with '+'.")
                    phone_number = None

            if phone_number:
                speak("What would you like to send?")
                message = takecommand().lower()
                if message == "none":
                    print("Could not get the message. Please try again.")
                else:
                    now = datetime.now()
                    send_time = now + timedelta(minutes=2)
                    kit.sendwhatmsg(phone_number, message, send_time.hour, send_time.minute)
                    speak(f"Message scheduled to {phone_number}.")

        elif "send email" in query:

            speak("Please provide the recipient's email ID.")
            recipient_email = input("Enter recipient's email address: ")

            speak("What is the subject of the email?")
            subject = takecommand().capitalize()

            speak("What content would you like to include in the email?")
            content = takecommand()

            speak("Would you like to attach any files? Type 'yes' or 'no'.")
            attach_files = takecommand().lower()

            # Get file paths directly from user input if they want to attach files
            if "yes" in attach_files:
                file_paths = input(
                    "Enter the file paths separated by commas (e.g., /path/to/file1, /path/to/file2): ").split(',')
                file_paths = [path.strip() for path in file_paths]
            else:
                file_paths = []

            try:
                msg = MIMEMultipart()
                msg['From'] = SENDER_EMAIL  # Load sender email from environment variable
                msg['To'] = recipient_email
                msg['Subject'] = subject
                msg.attach(MIMEText(content, 'plain'))

                # Attach files if file paths were provided
                for file_path in file_paths:
                    try:
                        with open(file_path, 'rb') as file:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(file.read())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition', f"attachment; filename={file_path.split('/')[-1]}")
                            msg.attach(part)
                    except Exception as file_error:
                        speak(f"An error occurred while attaching the file {file_path}: {file_error}")

                # Sending email
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Use environment variables for login credentials
                text = msg.as_string()
                server.sendmail(SENDER_EMAIL, recipient_email, text)
                server.quit()

                speak("The email has been sent successfully.")
            except Exception as e:
                speak(f"An error occurred while sending the email: {e}")

        elif "set alarm" in query:
            speak("Please tell me the time to set the alarm in the format HH:MM AM or PM")
            alarm_time = takecommand().lower()

            try:
                alarm_hour = int(alarm_time.split(":")[0])
                alarm_minute = int(alarm_time.split(":")[1].split()[0])
                alarm_period = alarm_time.split()[1]

                if alarm_period == "pm" and alarm_hour != 12:
                    alarm_hour += 12
                elif alarm_period == "am" and alarm_hour == 12:
                    alarm_hour = 0

                speak(f"Alarm set for {alarm_time}. I will notify you when it's time.")

                while True:
                    current_time = datetime.now()
                    if current_time.hour == alarm_hour and current_time.minute == alarm_minute:
                        speak("Time to wake up! Playing a random song for you.")
                        # Play a random song with autoplay enabled
                        play_random_song_on_youtube()
                        break

                    time.sleep(30)

            except ValueError:
                speak("I couldn't understand the time format. Please try again.")

        elif "joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "shutdown the system" in query:
            speak("Shutting down the system.")
            os.system("sudo shutdown -h now")

        elif "restart the system" in query:
            speak("Restarting the system.")
            os.system("sudo shutdown -r now")

        elif "sleep the system" in query:
            speak("Putting the system to sleep.")
            os.system("pmset sleepnow")

        elif "your name" in query:
            speak("its BINGO which stands for binary intellegance graphical neural operations")

        elif "switch the tab" in query:
            open_apps = subprocess.run(["osascript", "-e",
                                        'tell application "System Events" to get name of (every process whose background only is false)'],
                                       capture_output=True, text=True)
            app_list = open_apps.stdout.strip().split(", ")

            if app_list:
                speak("Here are the applications currently open:")
                for app in app_list:
                    speak(app)

                speak("Which application would you like to maximize?")
                app_to_open = takecommand().lower()

                found_app = False
                for app in app_list:
                    if app_to_open in app.lower():
                        os.system(f'osascript -e \'tell application "{app}" to reopen\'')
                        os.system(f'osascript -e \'tell application "{app}" to activate\'')
                        speak(f"Maximizing {app}.")
                        found_app = True
                        break

                if not found_app:
                    speak("Sorry, I couldn't find that application. Please try again.")
            else:
                speak("No applications are currently open.")

        elif "news" in query:
            speak("Fetching the latest news.")
            all_news = fetch_news()
            if all_news[0] == "No news articles found at the moment.":
                speak(all_news[0])
            else:
                while True:
                    random_news = random.sample(all_news, min(5, len(all_news)))
                    for i, news in enumerate(random_news, 1):
                        speak(f"Headline {i}: {news}")

                    speak("Would you like to hear more news?")
                    user_response = takecommand().lower()

                    if "no" in user_response:
                        speak("Okay, exiting news section.")
                        break
                    elif "yes" in user_response:
                        continue
                    else:
                        speak("I'm sorry, I didn't understand. Please say 'yes' or 'no'.")


        elif "no thanks" in query:
            speak("thank you sir have a great day")
            sys.exit()

 speak("Sir do you have any more work for me?")









