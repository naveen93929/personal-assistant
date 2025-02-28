import speech_recognition as sr
import pyttsx3
import requests
import wikipedia
import time 
import random
import webbrowser

 
# Initialize the recognizer
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening....")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I did not get that")
        speak("Sorry, I did not get that")
    return ""

# answer questions and open websites
def open_website(query):
    if "youtube" in query.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "google" in query.lower():
        webbrowser.open("https://www.google.com/")
    else:
        speak("Sorry, I can't open that website")

# Set Reminder
def set_reminder(reminder, delay):
    speak(f"Setting a reminder for {reminder} in {delay} seconds.")
    time.sleep(delay)
    speak(f"Reminder: {reminder}")

# jokes
jokes = ["Why don't scientists trust atoms? Because they make up everything!",
         "What do you get if you cross a cat with a dark horse? Kitty Perry!",
         "What do you call a pile of cats? A meowtain!",
         "What do you call a bear with no teeth? A gummy bear!",
         "What do you call a fish with no eyes? Fsh!"]

def tell_joke():
    joke = random.choice(jokes)
    speak(joke)

# weather update
def get_weather(city):
    api_key = "30d5568794b2120f1b36f5b3b9330c4d"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    weather_data = response.json()
    if weather_data["cod"] != "404":
        main = weather_data["main"]
        temperature = main["temp"]
        return f"The temperature in {city} is {temperature - 273.15:.2f}°C."
    else:
        return "City not found."

# search wikipedia
def search_wikipedia(query):
    result = wikipedia.summary(query, sentences=2)
    speak(result)

# read news headlines
def get_news():
    api_key = "0fcd8c2b822742f69a544ee0f1e196fe"
    url = f"http://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    news_data = response.json()
    headlines = [article["title"] for article in news_data["articles"][:5]]
    for headline in headlines:
        speak(headline)



def main():
    while True:
        speak("How can I help you today?")
        query = listen()

        if "exit" in query.lower():
            speak("Exiting the program. Goodbye!")
            print("Exiting the program...")
            break
        elif "open" in query.lower():
            open_website(query)
        elif "reminder" in query.lower():
            set_reminder("your task", 10)  
        elif "joke" in query.lower():
            tell_joke()
        elif "weather" in query.lower():
            speak("Which city?")
            city = listen()
            if city:
                weather_report = get_weather(city)
                speak(weather_report)
            else:
                speak("I didn't catch the city name.")
        elif "wikipedia" in query.lower():
            search_wikipedia(query)
        elif "news" in query.lower():
            get_news()
       

if __name__ == "__main__":
    main()
