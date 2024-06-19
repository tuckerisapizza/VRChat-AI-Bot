# Python program to translate
# speech to text and text to speech
 
 
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pygame import mixer, _sdl2 as devices
import os
import asyncio
from characterai import aiocai
from pythonosc import osc_server, udp_client
import vrchatapi
from vrchatapi.api import authentication_api, invite_api, notifications_api, worlds_api, instances_api
from vrchatapi.exceptions import UnauthorizedException
from vrchatapi.models.two_factor_auth_code import TwoFactorAuthCode
from vrchatapi.models.two_factor_email_code import TwoFactorEmailCode
import threading
import random
import time

#README

#i recommend you setup your audio pipelines before you even go installing packages
#speaker needs to be mapped to microphone using VB-Audio Cable (for text to speech)
#microphone needs to be mapped to speaker using a physical aux cable connecting a speaker output to microphone input (for speech recognition)

#after that, test if it works by playing a youtube video and see if the script detects the youtube video's audio and the bot responds to it
#then, install packages and replace neccessary values such as your VRChat login and character AI api key

#character AI api key can be found here (https://docs.kram.cat/) run the first script on this page, input the link they email you, and thats your key for line 74
#input a character ai character into line 70
#input your vrchat credentials into lines 125 and 126

#
global num
global aiinput
global speechrecdone
global timesent
global listencount
global chat
global resets
globals()["num"] = 1
globals()["resets"] = 0
globals()["aiinput"] = ""
globals()["speechrecdone"] = False
globals()["timesent"] = round(time.time(), 1)
globals()["listencount"] = 0

def filter(input):
    badword = False
    bad_words_list = ["porn", "p hub", "9/11", "hitler", "911", "nazi", "1940", "drug", "meth", "serial killer", "kill myself", "cannibalism","columbine","shoot", "cult", "minstrel","blackface","standoff", "murder", "bombing", "suicide", "massacre", "genocide", "zoophil", "knot", "canna", "nig", "fag", "adult content", "nsfw"] 
    for word in bad_words_list: #filters out really bad stuff
        if badword == False:
            if word in input.lower():
                badword = True
            else:
                badword = False
            
    return badword

def sendchatbox(aiinput):
    
    messagestring = "🐝Tigerbee Bot🐝\v╔══════╗\v%s\v╚══════╝" % (aiinput) #replace the first line with your bot's name
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000) # SENDS DATA TO VRCHAT OVER PARAMS FOCUS, FOCUSLEFT AND FOCUSRIGHT  #this is funny to see because i stole the code from my Muse VRChat implementation 
    client.send_message("/chatbox/input", [messagestring , True, False])
    print(messagestring)

async def cai():
    char = "-utjNm3ucG3AwUNA7VPGjN-6tB4LhoW0W4yjByGfWL8" #character AI character url goes here (found at the end of any chat url). default is tigerbee bot.
    #dHDnyegsNfHd4nGojcTmtEoVPtD3L-rxEWulLHgKLOU #might be gojo character ai
    #13bcwUru8Qg8BIKBO7NbsHaE3EVeVWlTx4QcV1sG6Oo #might be joe biden character ai
    client = aiocai.Client("CHARACTER AI KEY")  #CHARACTER AI API KEY GOES HERE

    me = await client.get_me()

    async with await client.connect() as chat:
        
        new, answer = await chat.new_chat(
            char, me.id
        )

        
        print(f'{answer.name}: {answer.text}')
        #SpeakText("Sorry, an error occured. Restarting. " + answer.text)
   #     SpeakText("Restarting. " + answer.text)
        if globals()["resets"] > 0:
            SpeakText("Character AI filtered out the prompt or the bot reset. Please try again.")
        else:
            SpeakText("Update applied and bot reset. " + answer.text) #says the bot's greeting message
        
        
        while True:    
            try:
                if globals()["speechrecdone"] == True:
                    sendchatbox("Thinking...") #lets users know the bot is thinking
                    globals()["speechrecdone"] = False
                    MyText = globals()["aiinput"]
                    isinputbad = filter(MyText)
                    if isinputbad:
                        SpeakText("Prompt is innapropriate. Please try again.")
                    else:
                        message = await chat.send_message(
                            char, new.chat_id, MyText
                        )
                        isresponsebad = filter(message.text)
                        if isresponsebad:
                            SpeakText("Response is innapropriate. Please try again.")
                        else:
                            print(f'{message.name}: {message.text}')
                            SpeakText(message.text)
                            globals()["speechrecdone"] = False
                await asyncio.sleep(0)
            except: #sometimes, character ai filters an entire request, crashing the script. we just start up a new one and add a tick to the reset counter. worked fine for me
                globals()["resets"] = globals()["resets"] + 1
                task2 = asyncio.create_task(cai())
                await asyncio.gather(task2)
                while True: #this code never runs, have it here just in case
                    print("something is fucked")

                
            
def checkinvites():
    configuration = vrchatapi.Configuration(
        username = 'VRChat Username',       #INPUT YOUR VRCHAT USERNAME
        password = 'VRChat Password',       #INPUT YOUR VRCHAT PASSWORD
    )

    with vrchatapi.ApiClient(configuration) as api_client:
    #    # Set our User-Agent as per VRChat Usage Policy
        api_client.user_agent = "VRChat AI Bot / public release / email goes here / made by tucker."

        # Instantiate instances of API classes
        auth_api = authentication_api.AuthenticationApi(api_client)
    
        try:
            # Step 3. Calling getCurrentUser on Authentication API logs you in if the user isn't already logged in.
            current_user = auth_api.get_current_user()
        except UnauthorizedException as e:
            if e.status == 200:
                if "Email 2 Factor Authentication" in e.reason:
                    # Step 3.5. Calling email verify2fa if the account has 2FA disabled
                    auth_api.verify2_fa_email_code(two_factor_email_code=TwoFactorEmailCode(input("Email 2FA Code: ")))
                elif "2 Factor Authentication" in e.reason:
                    # Step 3.5. Calling verify2fa if the account has 2FA enabled
                    auth_api.verify2_fa(two_factor_auth_code=TwoFactorAuthCode(input("2FA Code: ")))
                    current_user = auth_api.get_current_user()
                else:
                    print("Exception when calling API: %s\n", e)
        except vrchatapi.ApiException as e:
            print("Exception when calling API: %s\n", e)
        #
        print("Logged in as:", current_user.display_name)
        
        while(True):
            notifications = notifications_api.NotificationsApi(api_client).get_notifications()
            for notification in notifications:
                if notification.type == 'friendRequest':
                    notifications_api.NotificationsApi(api_client).accept_friend_request(notification.id)
                    print("accepted friend!")
                        
            time.sleep(5)  # Check for notifications every 5 seconds

def speechrec():
    while(True):    
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            
            globals()["listencount"] = globals()["listencount"] + 1
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)

            try:
                # Capture audio input
                audio = recognizer.listen(source, timeout=1.7, phrase_time_limit=8)  # Adjust timeout as needed

                print("Recognizing...")
                

                # Use Google Speech Recognition
                sentence = recognizer.recognize_google(audio)

                # Print recognized sentence
                print(f"Recognized: {sentence}")
                oldaiinput =  globals()["aiinput"]
                newaiinput = sentence
                globals()["aiinput"] = sentence
                if oldaiinput == newaiinput: 
                    globals()["speechrecdone"] = True
                else:
                    time.sleep(.1)
                    globals()["aiinput"] = sentence
                    globals()["speechrecdone"] = True

            except sr.WaitTimeoutError:
                if globals()["listencount"] > 10: #after 10 failed attempts, shows text box to get engagement back
                    sendchatbox("Hi, I'm Tigerbee bot!\vCome talk with me!\v(Read my bio)")
                    globals()["listencount"] = 0
            except sr.UnknownValueError:
                print("Speech recognition could not understand audio.")
                
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            
                    
                
        

def move():  
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    while (True):
        time.sleep(.13) #shorter time means faster movements, depends on machine speed tbh
        if globals()["speechrecdone"] == False: #only moves when the bot isnt thinking
                num = random.randrange(1, 160)
                
                
                
                # SENDS DATA TO VRCHAT OVER PARAMS FOCUS, FOCUSLEFT AND FOCUSRIGHT
                timesent2 = round(time.time(), 1)
                if num == 10:
                    client.send_message("/input/Jump", [1])
                    num2 = random.randrange(1,2)
                    #print("jump for " + str(num2) + " seconds")
                    currenttime2 = round(time.time(), 1)
                    while currenttime2 < timesent2 + num2:
                        currenttime2 = round(time.time(), 1)
                    client.send_message("/input/Jump", [0])
                
                if num == 60:
                    client.send_message("/input/MoveForward", [1])
                    num2 = random.randrange(1,2)
                    #print("moving forward for " + str(num2) + " seconds")
                    currenttime2 = round(time.time(), 1)
                    while currenttime2 < timesent2 + num2:
                        currenttime2 = round(time.time(), 1)
                    client.send_message("/input/MoveForward", [0])

                if num == 40:
                    client.send_message("/input/LookLeft", [1])
                    num2 = random.randrange(10, 75)
                    num3 = num2 / 100
                    #print("left for " + str(num3) + " seconds")
                    currenttime2 = round(time.time(), 1)
                    while currenttime2 < timesent2 + num3:
                        currenttime2 = round(time.time(), 1)
                    client.send_message("/input/LookLeft", [0])

                if num == 20:
                    client.send_message("/input/LookRight", [1])
                    num2 = random.randrange(10, 75)
                    num3 = num2 / 100
                    #print("right for " + str(num3) + " seconds")
                    currenttime2 = round(time.time(), 1)
                    while currenttime2 < timesent2 + num3:
                        currenttime2 = round(time.time(), 1)
                    client.send_message("/input/LookRight", [0])
                



            



def SpeakText(command):
    globals()["listencount"] = 0
    sendchatbox(command)
        # Initialize mixer with the correct device
    # Set the parameter devicename to use the VB-CABLE name from the outputs printed previously.
    mixer.init(devicename = "CABLE Input (VB-Audio Virtual Cable)") #outputs to the microphone
 
    tts = gTTS(command, lang='en')
    tts.save(str(globals()["num"]) + ".mp3")

    # Play the saved audio file
    mixer.music.load(str(globals()["num"]) + ".mp3")
    mixer.music.play()
    mixer.stop()
    globals()["num"] += 1
    
        
# Loop infinitely for user to
# speak

async def main():
    mixer.init()
    print("Outputs:", devices.audio.get_audio_device_names(False))
    mixer.quit()
    # Initialize the recognizer 
    r = sr.Recognizer() 

    
        # Create tasks for async functions
    
    task2 = asyncio.create_task(cai()) #yes, i did use chatgpt to help me manage the threads, thank u for asking

    # Run normal function in a separate thread
    thread = threading.Thread(target=speechrec)
    thread.start()
    thread2 = threading.Thread(target=checkinvites)
    thread2.start()
    thread3 = threading.Thread(target=move)
    thread3.start()

    # Let tasks run indefinitely without waiting for them to complete
    await asyncio.gather(task2)

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())