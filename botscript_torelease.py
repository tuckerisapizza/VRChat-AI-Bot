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
from vrchatapi.api import authentication_api, invite_api, notifications_api, worlds_api, instances_api, groups_api
from vrchatapi.exceptions import UnauthorizedException
from vrchatapi.models.two_factor_auth_code import TwoFactorAuthCode
from vrchatapi.models.two_factor_email_code import TwoFactorEmailCode
from vrchatapi.models.create_group_invite_request import CreateGroupInviteRequest


import threading
import random
import time

import credentials
 


# Function to convert text to
# speech
global num
global aiinput
global speechrecdone
global timesent
global listencount
global chat
global resets
global isemoting
global movementpaused
global title

globals()["num"] = 1
globals()["resets"] = 0
globals()["aiinput"] = ""
globals()["speechrecdone"] = False
globals()["timesent"] = round(time.time(), 1)
globals()["listencount"] = 0
globals()["isemoting"] = False
globals()["movementpaused"] = False
globals()["title"] = "🐝Tigerbee Bot🐝"

def filter(input):
    badword = False
    bad_words_list = [" edging "," penis ","mein kampf"," cult ", " touch ", " rape ", "daddy","jew","porn", "p hub", "9/11", "9:11", "hitler", "911", "nazi", "1940", "drug", "methan", "serial killer", "kill myself", "cannibalism","columbine", "minstrel","blackface","standoff", "murder", "bombing", "suicide", "massacre", "genocide", "zoophil", "knot", "canna", "nigg", "fag", "adult content", "nsfw"]
    for word in bad_words_list:
        if badword == False:
            if word in input.lower():
                badword = True
                print("BAD WORD FOUND " + word)
            else:
                badword = False
            
    return badword

def checkfocommands(combined, prompt, airesp):
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    response = combined.lower()

    globals()["isemoting"] = True
    if "forward" in response:
        client.send_message("/input/MoveForward", [1])
        time.sleep(2)
        client.send_message("/input/MoveForward", [0])
    if "backward" in response:
        client.send_message("/input/MoveBackward", [1])
        time.sleep(2)
        client.send_message("/input/MoveBackward", [0])
    if "left" in response:
        client.send_message("/input/LookLeft", [1])
        time.sleep(.45)       
        client.send_message("/input/LookLeft", [0])
    if "right" in response:
        client.send_message("/input/LookRight", [1])
        time.sleep(.45)       
        client.send_message("/input/LookRight", [0])
    if "play" in response and "spotify" in response:
        SpeakText("Sorry, Spotify support isn't currently available.")
        
    if "play" in response and "youtube" in response:
        SpeakText("Sorry, Youtube support isn't currently available.")
    if "pause" in response and "move" in response:
        globals()["movementpaused"] = True
        globals()["title"] = "Movement paused.\vSay `unpause movement`."
    if "unpause" in response and "move" in response:
        globals()["movementpaused"] = False
        globals()["title"] = "🐝Tigerbee Bot🐝"
    
       
          
    globals()["isemoting"] = False

def checkforemotes(response):
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    response = response.lower()
    emote = 0
    globals()["isemoting"] = True
    if "wave" in response:
        emote = 1
    if "clap" in response:
        emote = 2
    if "point" in response:
        emote = 3
    if "cheer" in response:
        emote = 4
    if "dance" in response:
        emote = 5
    if "backflip" in response or "flip" in response:
        emote = 6
    if "kick" in response:
        emote = 7
    if "die" in response:
        emote = 8
    if not emote == 0:
        # SENDS DATA TO VRCHAT OVER PARAMS FOCUS, FOCUSLEFT AND FOCUSRIGHT     
        client.send_message("/avatar/parameters/VRCEmote", [int(emote)])
        print("emote # " + str(emote))
        time.sleep(2)
        client.send_message("/avatar/parameters/VRCEmote", [int(0)])      
    globals()["isemoting"] = False

def sendchatbox(aiinput):
    
    messagestring = "%s\v╔═══════╗\v%s\v╚═══════╝" % (globals()["title"], aiinput)
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000) # SENDS DATA TO VRCHAT OVER PARAMS FOCUS, FOCUSLEFT AND FOCUSRIGHT     
    client.send_message("/chatbox/input", [messagestring , True, False])
    print(messagestring)

async def cai():
    char = credentials.CAI_CHARACTER
    # char = "-utjNm3ucG3AwUNA7VPGjN-6tB4LhoW0W4yjByGfWL8" old tigerbee bot
    #dHDnyegsNfHd4nGojcTmtEoVPtD3L-rxEWulLHgKLOU
#13bcwUru8Qg8BIKBO7NbsHaE3EVeVWlTx4QcV1sG6Oo
    client = aiocai.Client(credentials.CAI_API_KEY)

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
            SpeakText("Updated and reset bot! " + answer.text)
            
        
        
        while True:    
            try:
                if globals()["speechrecdone"] == True:
                    sendchatbox("Thinking...")
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
                            checkforemotes(message.text + MyText)
                            checkfocommands(message.text + MyText,MyText,message.text)
                           
                            globals()["speechrecdone"] = False
                await asyncio.sleep(0)
            except:
                globals()["resets"] = globals()["resets"] + 1
                task2 = asyncio.create_task(cai())
                await asyncio.gather(task2)
                while True:
                    asynctasklol = ""   

                
            
def checkinvites():
    configuration = vrchatapi.Configuration(
        username = credentials.VRCHAT_USER,
        password = credentials.VRCHAT_PASSWORD,
    )

    with vrchatapi.ApiClient(configuration) as api_client:
    #    # Set our User-Agent as per VRChat Usage Policy
        api_client.user_agent = credentials.USER_AGENT

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
            try:
                notifications = notifications_api.NotificationsApi(api_client).get_notifications()
                for notification in notifications:
                    if notification.type == 'friendRequest':
                        notifications_api.NotificationsApi(api_client).accept_friend_request(notification.id)
                        print("accepted friend!")
                        invitereq = CreateGroupInviteRequest(notification.sender_user_id, True)
                        groups_api.GroupsApi(api_client).create_group_invite("grp_ed3c9205-ab1c-4564-840d-526d188ab7bf", invitereq)
                            
                time.sleep(7)  # Check for notifications every 5 seconds
            except:
                print("notif error")

def speechrec():
    while(True):    
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            
            globals()["listencount"] = globals()["listencount"] + 1
            # Adjust for ambient noise
           

            try:
                # Capture audio input
                audio = recognizer.listen(source, timeout=2.5, phrase_time_limit=8)  # Adjust timeout as needed

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
                if globals()["listencount"] > 10:
                    sendchatbox("Hi, I'm Tigerbee bot!\vCome talk with me!\v(Read my bio)")
                    globals()["listencount"] = 0
            except sr.UnknownValueError:
                print("Speech recognition could not understand audio.")
                
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            
                    
                
        

def move():  
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    while (True):
        time.sleep(.13)
        if globals()["speechrecdone"] == False and globals()["isemoting"] == False and globals()["movementpaused"] == False:
            
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
    mixer.init(devicename = "CABLE Input (VB-Audio Virtual Cable)", frequency=48510)
 
    tts = gTTS(command.replace(":", " colon "), lang='en')
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
    
    task2 = asyncio.create_task(cai())

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
