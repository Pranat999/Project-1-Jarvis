import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests

#pip install pocketsphinx  (not needed as of now)

recognizer=sr.Recognizer()
engine=pyttsx3.init() #initialises pyttsx3
newsapi = "e78bc1faf81b4111aa78c69ffb0db632"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def ProcessCommand(c):
    print(f"Processing command: {c}")  # Debugging output
    
    if("open google" in c.lower()):
        webbrowser.open("https://google.com")
    elif("open youtube" in c.lower()):
        webbrowser.open("https://youtube.com")

    elif("play" in c.lower()):
        song = c.split('play')[1].strip()  # Splitting and joining the parts after "play"
        #if c="can you please play ain't no sunshine"
        #song.split('play'): ['can you please ', ' ain't no sunshine']
        # [1] : " ain't no sunshine"
        # .strip() : removes leading white spaces from both start and end of string, thus: "ain't no sunshine"  
        print(f"Requested song: {song}")  # Debugging output
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            print(f"Opening link: {link}")  # Debugging output
            webbrowser.open(link)
        elif song.title() in musicLibrary.music: #song.title() will capitalize first letter of each word in the string
            link = musicLibrary.music[song.title()]
            print(f"Opening link: {link}")  # Debugging output
            webbrowser.open(link)
        else:
            print(f"Song '{song}' not found in music library.")  # Debugging output
    
    elif("news" in c.lower()):
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if(r.status_code == 200):
            #Parse the JSON response
            data = r.json()

            #Extract the articles
            articles = data.get('articles',[])

            #Speak the headlines
            for article in articles:
                speak(article['title'])

    else:
        #let openAI handle the request
        pass
        

if __name__ == "__main__":
    speak("Initialising Jarvis...")
    while True:
        # Listen for the wake word 'Jarvis'
        # obtain audio from the microphone 
        r = sr.Recognizer()

        print("recognizing..")
        try:
            with sr.Microphone() as source:
                print("Listening..")
                audio = r.listen(source ,timeout=5, phrase_time_limit=5) 
                
            word = r.recognize_google(audio)
            if("jarvis" in word.lower()):
                speak("Hey, how can I help you?")   
                #Listen for command 
                with sr.Microphone() as source:
                    print("Jarvis Active..")
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)

                    ProcessCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))