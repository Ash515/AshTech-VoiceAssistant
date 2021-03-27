import pyjokes as pyjokes
import pywhatkit
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
import ecapture as ec
import wolframalpha
import json
import socket
import re
import requests
import pyaudio
import random
import headlines
import getpass
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import librosa
import soundfile
import numpy as np
import pickle
import glob
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import pickle
from scipy.io import wavfile
from bs4 import BeautifulSoup
import requests
import platform
import Bday
import pyshorteners
import pyperclip
from tkinter import *
import pyautogui
from PIL import Image, ImageGrab 
import qrcode

pyttsx3.speak("Enter your password")
inpass = getpass.getpass("Enter your password :")
apass = "ashwin"
if inpass != apass:
    pyttsx3.speak("Incorrect Password Try Again ")
    exit()
pyttsx3.speak("Access Granted")

print("Loading your AI personal assistant - Ashtech ")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[0].id')

root = Tk()
root.geometry("400x200")
root.title("URL Shortener")
root.configure(bg='#49A')
url = StringVar()
url_address = StringVar()

def speak(text):
    engine.say(text)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello,Good Morning")
        print("Hello,Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")
        print("Hello,Good Evening")


def take_First_Command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        with open("audio_file.wav", "wb") as file:
            file.write(audio.get_wav_data())
        user_mood()

        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said : {statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement


def whatsapp(to, message):
    person = [to]
    string = message
    chrome_driver_binary = "C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe"
    # Selenium chromedriver path
    driver = webdriver.Chrome(chrome_driver_binary)
    driver.get("https://web.whatsapp.com/")
    #wait = WebDriverWait(driver,10)
    sleep(15)
    for name in person:
        print('IN')
        user = driver.find_element_by_xpath("//span[@title='{}']".format(name))
        user.click()
        print(user)
        for _ in range(10):
            text_box = driver.find_element_by_xpath(
                '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            text_box.send_keys(string)
            sendbutton = driver.find_elements_by_xpath(
                '//*[@id="main"]/footer/div[1]/div[3]/button')[0]
            sendbutton.click()


def user_mood():
    with soundfile.SoundFile('audio_file.wav') as s_file:
        x = s_file.read(dtype="float32")
        sample_rate = s_file.samplerate
        # x,sample_rate=soundfile.read(s_file)
        chroma = True
        mfcc = True
        mel = True
        if chroma:
            stft = np.abs(librosa.stft(x))
        result = np.array([])
        if mfcc:
            mfccs = np.mean(librosa.feature.mfcc(y=x,
                                                 sr=sample_rate,
                                                 n_mfcc=40).T,
                            axis=0)
            result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(S=stft,
                                                         sr=sample_rate).T,
                             axis=0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(x, sr=sample_rate).T,
                          axis=0)
            result = np.hstack((result, mel))

    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
        result = np.array(result)
        result = result.reshape(180, 1)
        result = result.transpose()
        pred = model.predict(result)
        if (pred == 1):
            speak('You seem happy today')
            print('You seem happy today :)')

        elif (pred == 0):
            speak(' Should I tell you some jokes to make your mood before')
            print('Should I tell you some jokes to make your mood before')
            statement1 = takeCommand().lower()
            if 'yes' in statement1:
                joke = pyjokes.get_joke('en', 'all')
                print(joke)
                speak(joke)
            else:
                return


# function for coin toss task


def htLine1():
    speak("It's " + coinRes)


def htLine2():
    speak("You got " + coinRes)


def htLine3():
    speak("It landed on " + coinRes)


def defination(searchtext):
    url = 'https://www.dictionary.com/browse/'
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    })
    wikistr = wikipedia.summary(searchtext, sentences=3)
    index = wikistr.find(searchtext)
    if (index != -1):
        wikidef = wikipedia.summary(searchtext, sentences=3)
        return (wikidef)
    else:
        req = requests.get(url + searchtext, headers)
        soup = BeautifulSoup(req.content, 'html.parser')

        mydivs = soup.findAll("div", {"value": "1"})[0]

        for tags in mydivs:
            meaning = tags.text
        return (meaning)

# Url Shortener

def urlshortener():
    urladdress = url.get()
    url_short = pyshorteners.Shortener().tinyurl.short(urladdress)
    url_address.set(url_short)

def copyurl():
    url_short = url_address.get()
    pyperclip.copy(url_short)  


# function for dino game
def click(key):
    pyautogui.keyDown(key)
    return

def isCollision(data):
# Check colison for birds
    for i in range(530,560):
        for j in range(160, 195):
            if data[i, j] < 100:
                click("down")
                return

# Check colison for cactus
    for i in range(530, 620):
        for j in range(200, 230):
            if data[i, j] < 100:
                click("up")
                return
    return

speak("Loading your AI personal assistant AshTech")
wishMe()

user_dct = dict()

prev_users = open('users.txt', 'r')
try:
    for line in prev_users:
        prev_lst = line.strip().split()
        user_dct[prev_lst[0]] = int(prev_lst[1])
except:
    pass
prev_users.close()

user_dct[platform.node()] = user_dct.get(platform.node(), 0) + 1

new_users = open('users.txt', 'w')
for k, v in user_dct.items():
    print(k, v, file=new_users)
new_users.close()

if __name__ == '__main__':

    statement = take_First_Command().lower()
    while True:

        if statement == 0:
            continue

        if "good bye" in statement or "ok bye" in statement or "stop" in statement or "quit" in statement or "close" in statement:
            print('your personal assistant Ashtech is shutting down, Good bye')
            speak(
                'your personal assistant Ashtech  is shutting down, Good bye')
            break

        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube is open now")
            time.sleep(5)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is open now")
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail open now")
            time.sleep(5)

        elif 'covid-19 tracker' in statement:
            webbrowser.open_new_tab(
                "https://news.google.com/covid19/map?hl=en-IN&gl=IN&ceid=IN%3Aen"
            )
            speak("covid-19 tracker is open now")
            time.sleep(5)

        elif "shoping" in statement or 'shopping' in statement:
            websites = ['amazon', 'flipkart', 'myntra', 'limeroad']
            print('\n'.join(websites))
            speak("nice mood sir!, what do you want to open?")
            user_ip = takeCommand().lower().replace(' ', '')

            for website in websites:
                if website in user_ip:
                    webbrowser.open(website + '.com')

            speak("here you are sir")

        elif 'online courses' in statement or 'course' in statement:
            platforms = [
                'coursera', 'udemy', 'edx', 'skillshare', 'datacamp', 'udacity'
            ]
            speak("Select a platform that you prefer : ")
            print("\n".join(platforms))
            statement1 = takeCommand().lower()
            if statement1 == 0:
                continue
            if 'coursera' in statement1:
                webbrowser.open_new_tab("https://www.coursera.org")
                speak("Coursera is open now")
                time.sleep(2)
            elif 'udemy' in statement1:
                webbrowser.open_new_tab("https://www.udemy.com")
                speak("udemy is open now")
                time.sleep(2)
            elif 'edx' in statement1:
                webbrowser.open_new_tab("https://www.edx.org/")
                speak("edx is open now")
                time.sleep(2)
            elif 'skillshare' in statement1:
                webbrowser.open_new_tab("https://www.skillshare.com")
                speak("skill share is open now")
                time.sleep(2)
            elif 'datacamp' in statement1:
                webbrowser.open_new_tab("https://www.datacamp.com")
                speak("datacamp is open now")
                time.sleep(2)
            elif 'udacity' in statement1:
                webbrowser.open_new_tab("https://www.udacity.com")
                speak("udacity is open now")
                time.sleep(2)
            else:
                speak("Sorry we couldn't find your search!!!")
            time.sleep(3)

        elif 'jobs' in statement or 'job' in statement or 'job recommandation' in statement or 'work' in statement:
            platforms = [
                'linkedin', 'indeed', 'glassdoor', 'hackerrank', 'naukri',
                'intern shala'
            ]
            speak("Select a platform that you prefer:")
            print('\n'.join(platforms))
            statement1 = takeCommand().lower()
            if (statement1 == 0):
                continue
            if 'linkedIn' in statement1:
                webbrowser.open_new_tab("https://www.linkedin.com/jobs")
                speak("LinkedIn is open now")
                time.sleep(2)
            elif 'indeed' in statement1:
                webbrowser.open_new_tab("https://www.indeed.com/jobs")
                speak("Indeed is open now")
                time.sleep(2)
            elif 'glassdoor' in statement1:
                webbrowser.open_new_tab("https://www.glassdoor.com/jobs")
                speak("Glassdoor is open now")
                time.sleep(2)
            elif 'hackerrank' in statement1:
                webbrowser.open_new_tab(
                    "https://www.hackerrank.com/jobs/search")
                speak("HackerRank is open now")
                time.sleep(2)
            elif 'naukri' in statement1:
                webbrowser.open_new_tab("https://www.naukri.com/jobs")
                speak("Naukri is open now")
                time.sleep(2)
            elif 'intern shala' in statement:
                webbrowser.open_new_tab('internshala.com')
                speak('Intern Shala is open now')
                time.sleep(2)
            else:
                speak("Sorry we couldn't find your search!!!")
            time.sleep(3)

        elif 'news' in statement or 'news headline' in statement or 'top news' in statement or 'some news' in statement:
            speak('Here are some headlines from the India today')

            res = requests.get('https://www.indiatoday.in/top-stories')
            soup = BeautifulSoup(res.text, 'lxml')

            news_box = soup.find('div', {'class': 'top-takes-video-container'})
            all_news = news_box.find_all('p')

            for news in all_news:
                print('\n' + news.text)
                speak(news.text)
                print()
                time.sleep(6)
            time.sleep(8)

        elif 'movie ticket booking' in statement or 'movie booking' in statement or 'movie ticket' in statement:
            speak('Here are some top websites for ticket booking')
            webbrowser.open_new_tab("https://in.bookmyshow.com/")
            speak(" Book my show website is open now")
            time.sleep(2)

        elif 'train ticket booking' in statement or 'train booking' in statement or 'train ticket' in statement or 'train ticket' in statement:
            speak('Here are some top websites for tarin ticket booking')
            webbrowser.open_new_tab("https://www.easemytrip.com/railways/")
            speak(" Ease My trip website is open now, have a good journey !")
            time.sleep(2)

        elif 'bus ticket booking' in statement or 'bus booking' in statement or 'bus ticket' in statement:
            speak('Here are some top websites for bus ticket booking')
            webbrowser.open_new_tab("https://www.redbus.in")
            speak(" Red bus website is open now, have a good journey !")
            time.sleep(2)

        elif 'airplane ticket booking' in statement or 'airplane booking' in statement or 'airplane ticket' in statement:
            speak('Here are some top websites for airplane ticket booking')
            webbrowser.open_new_tab("https://www.goindigo.in")
            speak(" Indigo website is open now, have a good journey !")
            time.sleep(2)

        elif "hotel" in statement or "hotel booking" in statement:
            speak('Opening go ibibo .com')
            webbrowser.open_new_tab('goibibo.com/hotels')

        elif 'top engineering colleges in india' in statement or 'indian engineering college' in statement or 'engineering college' in statement:
            webbrowser.open_new_tab(
                "https://www.shiksha.com/b-tech/ranking/top-engineering-colleges-in-india/44-2-0-0-0"
            )
            speak("Colleges as per NIRF Ranking are open on Shiksha website!")
            time.sleep(2)

        elif 'top medical colleges in india' in statement or 'indian medical college' in statement or 'medical college' in statement:
            speak('Here are some top Medical Colleges in India')
            webbrowser.open_new_tab(
                "https://medicine.careers360.com/colleges/ranking")
            speak("Colleges as per NIRF rankings are opened!")
            time.sleep(2)

        elif 'top science colleges in india' in statement or 'indian science college' in statement or 'science college' in statement:
            speak('Here are some top website for Science Colleges in India')
            webbrowser.open_new_tab(
                "https://collegedunia.com/science-colleges")
            speak(" College Dunia website is opened!")

        elif 'top law colleges in india' in statement or 'indian law college' in statement or 'law college' in statement:
            speak('Here are some top website for law Colleges in India')
            webbrowser.open_new_tab(
                "https://www.collegedekho.com/law-humanities/law-colleges-in-india/"
            )
            speak(" College Deko website is opened!")
            time.sleep(2)

        elif 'top research colleges in india' in statement or 'indian research college' in statement or 'research college' in statement:
            speak('Here are some top website for Research Colleges in India')
            webbrowser.open_new_tab(
                "https://www.biotecnika.org/2019/09/top-govt-research-institutes-present-in-india-top-10-list/"
            )
            speak("Biotechnika website is opened!")
            time.sleep(2)

        elif "weather" in statement:

            api_key = "8ef61edcf1c576d65d836254e11ea420"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                print(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " + str(current_humidiy) +
                      "\n description  " + str(weather_description))
                speak(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " + str(current_humidiy) +
                      "\n description = " + str(weather_description))

        elif 'time' in statement:
            strTime = datetime.datetime.now().strftime("%I:%M:%S %p")
            print(f"the time is {strTime}")
            speak(f"the time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak(
                'I am Ashwin friend Ashtech version 1 point O your persoanl assistant. I am programmed to minor tasks like'
                'opening youtube,google chrome,gmail and stackoverflow ,predict time,take a photo,search wikipedia,predict weather'
                'in different cities , get top headline news from times of india and you can ask me computational or geographical questions too!'
            )

        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I was built by Ashwin Kumar Ramaswamy")
            print("I was built by Ashwin Kumar Ramaswamy")

        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            speak("Here is stackoverflow")

        elif 'news' in statement:
            news = webbrowser.open_new_tab(
                "https://timesofindia.indiatimes.com/home/headlines")
            speak(
                'Here are some headlines from the Times of India,Happy reading'
            )
            speak(
                'If you like the headline, say "visit" to open the page and read details'
            )
            headlines = headlines.get_headlines(
                "https://timesofindia.indiatimes.com/home/headlines")
            for i in range(15):
                speak(headlines['text'][i])
                command = takeCommand()
                if 'visit' in command:
                    webbrowser.open_new_tab(headlines['link'][i])
                    break
                elif 'stop' in command:
                    break
                time.sleep(5)
            time.sleep(6)

        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0, "robo camera", "img.jpg")

        elif 'search' in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'flip the coin' in statement or 'toss the coin' in statement or 'toss a coin' in statement:
            chances = ['Heads', 'Tails']
            coinRes = random.choice(chances)
            picLine = random.randint(1, 3)
            lines = [htLine1, htLine2, htLine3]
            lines[picLine - 1]()

        elif 'dice' in statement:
            num = random.randint(1, 6)
            speak("Your dice number is " + str(num))

        elif 'url shortener' in statement:
            Label(root, text=" URL Shortener ", font = ("Arial bold", 13)).place(x=140,y=15)
            Label(root,text = 'Enter URL :', font = ("poppins",11)).place(x=45,y=65)
            Entry(root, textvariable=url, width = 35).place(x=145,y=67)
            Label(root,text = 'Short URL :', font = ("poppins", 11)).place(x=45,y=100)
            Entry(root, textvariable=url_address, width = 35).place(x=145,y=102)
            Button(root, text=" Shorten URL ", command=urlshortener).place(x=105,y=140)  
            Button(root, text=" Copy URL ", command=copyurl).place(x=205,y=140)      
            root.mainloop()

        elif 'hostname and ip' in statement or 'host name and ip' in statement:
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            print("Host-name: " + host_name)
            print("IP address: " + host_ip)
            speak("Your host name is" + host_name + "and ip address is" +
                  host_ip)

        elif 'on screen keyboard' in statement or 'onscreen keyboard' in statement:
            subprocess.run('osk', shell=True)

        elif 'cmd' in statement or 'command prompt' in statement or 'terminal' in statement:
            os.system("start cmd")

        elif 'module in python' in statement or 'pip list' in statement or 'libraries in python' in statement or 'module installed in python' in statement:
            subprocess.run('pip list', shell=True)
            speak("Printing all the modules installed in Python")

        # Hide and unhide files and folder
        elif 'hide folder' in statement or 'hide all files' in statement:
            os.system('attrib +h /s /d')
            speak("sir, all the files in this folder are now hidden.")

        elif 'unhide files' in statement or 'visible to everyone' in statement:
            os.system('attrib -h /s /d')
            speak("sir, all the files in this folder are now visible to everyone.")

        elif 'generate qr code' in statement:
            img = qrcode.make("https://github.com/Ash515/AshTech-AI_Personal_Voice_Assistant/")
            img.save("repo_qr_code.png")
            subprocess.run('repo_qr_code.png', shell='True')

        elif 'take screenshot' in statement or 'capture screen' in statement:
            print('Taking screenshot in 3 second')
            speak('Taking screenshot in 3 second')
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save('screenshot.png')
            subprocess.run('screenshot.png', shell='True')

        elif 'dinosaur game' in statement or 'chrome dino' in statement:
            print("Hey, Chrome dino game will start in 8 sec make sure your internet is off")
            time.sleep(9)
            click('up') 
            
            while True:
                image = ImageGrab.grab().convert('L')  
                data = image.load()
                isCollision(data)

        elif 'volume up' in statement or 'increase volume' in statement:
            pyautogui.press('volumeup')

        elif 'volume down' in statement or 'decrease volume' in statement or 'lower the volume' in statement:
            pyautogui.press('volumedown') 

        elif 'volume mute' in statement or 'turn off the volume' in statement or 'mute' in statement:
            pyautogui.press('volumemute')

        elif 'wi-fi and their password' in statement or 'wi-fi password' in statement:
            command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
            profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

            wifi_list = list()

            if len(profile_names) != 0:
                for name in profile_names:
                    wifi_profile = dict()
                    profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        
                    if re.search("Security key           : Absent", profile_info):
                        continue

                    else:
                        wifi_profile["ssid"] = name
                        profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
                        password = re.search("Key Content            : (.*)\r", profile_info_pass)
            
                        if password == None:
                            wifi_profile["password"] = None
                        else:
                            wifi_profile["password"] = password[1]
        
                        wifi_list.append(wifi_profile)


            with open('wifi_passwords.txt', 'w+') as fh:
                for x in wifi_list:
                    fh.write(f"Wifi_Name: {x['ssid']}\nPassword: {x['password']}\n")

            with open('wifi_passwords.txt', 'rb') as fh:
                    speak('Successfully stored all the wifi passwords in txt file')
                    subprocess.run('wifi_passwords.txt', shell=True)

        elif 'ask' in statement:
            speak(
                'I can answer to computational and geographical questions and what question do you want to ask now'
            )
            question = takeCommand()
            app_id = "R2K75H-7ELALHR35X"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)

        elif 'jokes' in statement or 'joke' in statement:
            joke = pyjokes.get_joke('en', 'all')
            print(joke)
            speak(joke)

        elif 'pycharm' in statement or 'open pycharm' in statement:
            os.startfile('pycharm')
            speak("pycharm is open now")

        elif 'visual studio code' in statement or 'open code' in statement or 'code' in statement or 'visual code' in statement:
            os.startfile('code')
            speak('visual studio code is open now')

        elif 'on youtube' in statement or 'youtube' in statement:
            statement = statement.replace("youtube", "")
            pywhatkit.playonyt(statement)
            speak('here you are sir!')
            time.sleep(120)

        elif 'what is my current location' in statement or 'what is my location' in statement or 'where am I' in statement:
            ip = "https://api.ipify.org/"
            ip_r = requests.get(ip).text

            geoip = "http://ip-api.com/json/" + ip_r
            geo_r = requests.get(geoip)
            geo_json = geo_r.json()

            print(
                f"Your current location is {geo_json['city']}, {geo_json['regionName']}, {geo_json['country']} {geo_json['zip']}"
            )
            speak(
                f"Your current location is {geo_json['city']}, {geo_json['regionName']}, {geo_json['country']} {geo_json['zip']}"
            )

        elif "notepad" in statement:
            speak("Opening Notepad")
            os.system("start Notepad")

        elif "outlook" in statement:
            speak("Opening Microsoft Outlook")
            os.system("start outlook")

        elif "word" in statement:
            speak("Opening Word")
            os.system("start winword")

        elif "paint" in statement:
            speak("Opening Paint")
            os.system("start mspaint")

        elif "excel" in statement:
            speak("Opening Excel")
            os.system("start excel")

        elif "start chrome" in statement:
            speak("Opening Google Chrome")
            os.system("start chrome")

        elif 'chrome in incognito mode' in statement or 'chrome in incognito' in statement:
            speak("Opening Google Chrome in Incognito mode")
            os.system('start chrome -incognito')

        elif "power point" in statement or "powerpoint" in statement or "ppt" in statement:
            speak("Opening Notepad")
            os.system("start powerpnt")

        elif "edge" in statement:
            speak("Opening Microsoft Edge")
            os.system("start msedge")

        elif "snipping tool" in statement:
            speak("Opening Snipping Tool")
            os.system("start snippingtool")

        elif "show deleted files" in statement or "Recycle Bin" in statement or "Delete files" in statement or "search deleted files" in statement:
            speak("Opening Recycle Bin")
            os.system("start shell:RecycleBinFolder")

        elif "calculator" in statement:
            speak("Opening Calculator")
            os.system("start calc")

        elif "log off" in statement or "sign out" in statement:
            speak(
                "Ok , your pc will log off in 10 sec make sure you exit from all applications"
            )
            subprocess.call(["shutdown", "/l"])

        # Writing notes
        elif "write a note" in statement:
            speak("What should i write, sir")
            print("J: What should i write, sir")
            note = takeCommand()
            file = open('jarvis.txt', 'w')
            speak("Sir, Should i include date and time")
            print("J: Sir, Should i include date and time")
            snfm = takeCommand()
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now()
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)

        # Showing note
        elif "show the note" in statement:
            speak("Showing Notes")
            print("J: Showing Notes")
            file = open("jarvis.txt", "r")
            print(file.read())
            speak(file.read(6))

        # whatsapp messaging
        elif 'whatsapp' in statement:
            try:
                print(
                    "J: To whom should i send? Can you please type in the name."
                )
                speak(
                    "To whom should i send? Can you please type in the name.")
                to = input('Name: ')
                print(
                    "J: What should i send? Can you please type in the message."
                )
                speak(
                    "What should i send? Can you please type in the message.")
                content = input("Enter the message: ")
                speak('You will have to scan for whatsapp web. ')
                print('J: You will have to scan for whatsapp web. ')
                whatsapp(to, content)
                speak("Message has been sent !")
                print("* J: Message has been sent !")
            except Exception as e:
                print(e)
                speak("I am not able to send this message")

        elif 'travel' in statement or 'cab-booking' in statement or 'trip' in statement or 'ola' in statement or 'uber' in statement or 'Cab' in statement:
            speak('It seems you are interested in travelling somewhere'
                  'Want to Use Cab Sevices or Travel long distanced Trip')
            print("Cab Sevices or Travel long distanced Trip")
            travelask = takeCommand().lower()

            if "travel-long" or "distanced-trip" or "trip" in travelask:
                websites = ['makemytrip', 'booking', 'airbnb', 'Trivago']
                print('\n'.join(websites))
                speak("what do you want to open?")
                user_ip = takeCommand().lower().replace(' ', '')
                for website in websites:
                    if website in user_ip:
                        speak('Opening' + str(website))
                        webbrowser.open(website + '.com')

            elif "cab-services" or "cab" in travelask:
                print("Want to use Ola or Uber")
                speak('Want to use Ola or Uber')
                travelask2 = takeCommand().lower()
                if "ola" in travelask2:
                    webbrowser.open_new_tab("https://www.olacabs.com")
                    speak('Ola website is open now')
                elif "uber" in travelask2:
                    webbrowser.open_new_tab("https://www.uber.com/in/en/")

                    speak('Uber website is open now')

            elif 'search' in statement or 'defination' in statement:
                speak('I guess you want to search defination'
                      'What do you want to search about sir')
                print("What do you want to search about sir")
                definationask = takeCommand().lower()
                finalmeaning = defination(definationask)
                print(finalmeaning)
                speak(finalmeaning)

                speak('Uber website is open now')

        elif 'system' in statement or 'system details' in statement or 'hardware' in statement:
            plat_det = platform.uname()
            print('User : ', plat_det.node)
            print('System :', plat_det.system, plat_det.release,
                  plat_det.version)
            print('Machine :', plat_det.machine)
            print('Processor : ', plat_det.processor)
            speak(plat_det.node)
            speak(plat_det.system)
            speak(plat_det.release)
            speak(plat_det.version)
            speak(plat_det.machine)
            speak(plat_det.processor)

        elif 'current user' in statement:
            speak('Currently')
            speak(platform.node())
            speak('is logged in and has logged in')
            speak(user_dct[platform.node()])
            speak('times till now')

        speak("Tell me how can I help you now?")
        statement = takeCommand().lower()

time.sleep(3)
