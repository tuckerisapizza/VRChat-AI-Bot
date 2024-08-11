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
from pydub import AudioSegment
import numpy as np


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
global consoleenabled

globals()["num"] = 1
globals()["resets"] = 0
globals()["aiinput"] = ""
globals()["speechrecdone"] = False
globals()["timesent"] = round(time.time(), 1)
globals()["listencount"] = 0
globals()["isemoting"] = False
globals()["movementpaused"] = False
globals()["title"] = "🐝Tigerbee Bot🐝"
globals()["consoleenabled"] = False

#debug variables
global printnumgen
globals()["printnumgen"] = False
global printtextbox
globals()["printtextbox"] = True
global botenabled
globals()["botenabled"] = True
global speechregenabled
globals()["speechregenabled"] = True
global notiflog
globals()["notiflog"] = False





def filter(input):
    badword = False
    bad_words_list = ["niger","cool kids club","kkk","ku klux klan","flustered","suck my dick","reagan","catheter","sexual play","intimate","vibrator","dildo","adult toy","holocaust","innards", "child porn", "innapropriate", "turns me on", " tickl", " explicit", " gape", " gaping", " fetish"," fart", " pee"," horny"," terroris","september 11th","bent over","inside of me","bend over","hemorrhoids"," piss","golden shower"," feces"," munting"," faeces"," kink","my girlfriend","my ai girlfriend", "be mine","xxx", "make love","do anything now"," illegal "," slur","blushes"," intercourse ","moon cricket"," bomb", " assassinate "," sex "," edging "," penis ","mein kampf"," cult ", " touch", " rape ", "daddy","jew"," porn", "p hub", "9/11", "9:11", "hitler", "911", "nazi", "1940", " drug", "methan", "serial killer", "kill myself", "cannibalism","columbine", "minstrel","blackface","standoff", "murder", "bombing", "suicide", "massacre", "genocide", "zoophil", "knot", "canna", " nigg", " fag", "adult content", "nsfw"]
    for word in bad_words_list:
        if badword == False:
            if word in input.lower():
                badword = True
                print("BAD WORD FOUND " + word)
            else:
                badword = False
            
    return badword

def debugcommandscheck(text):
    if "printnumgen" in text:
        if globals()["printnumgen"]:
            globals()["printnumgen"] = False
        else:
            globals()["printnumgen"] = True
        print(globals()["printnumgen"])

    if "botenabled" in text:
        if globals()["botenabled"]:
            globals()["botenabled"] = False
        else:
            globals()["botenabled"] = True
        print(globals()["botenabled"])

    if "printtextbox" in text:
        if globals()["printtextbox"]:
            globals()["printtextbox"] = False
        else:
            globals()["printtextbox"] = True
        print(globals()["printtextbox"])

    if "speechregenabled" in text:
        if globals()["speechregenabled"]:
            globals()["speechregenabled"] = False
        else:
            globals()["speechregenabled"] = True
        print(globals()["speechregenabled"])

    if "notiflog" in text:
        if globals()["notiflog"]:
            globals()["notiflog"] = False
        else:
            globals()["notiflog"] = True
        print(globals()["notiflog"])

    if "movement" in text:
        if globals()["movementpaused"]:
            globals()["movementpaused"] = False
        else:
            globals()["movementpaused"] = True
        print(globals()["movementpaused"])

    if "speechrecdone" in text:
        if globals()["speechrecdone"]:
            globals()["speechrecdone"] = False
        else:
            globals()["speechrecdone"] = True
        print(globals()["speechrecdone"])
    

def checkforreset(text):
    response = text.lower()
    if (("reset" in response or "restart" in response) and ("box" in response or "bot" in response or "bbott" in response or "Bebop" in response or "butt" in response)):
        return True
    else:
        return False

def checkfocommands(combined, prompt, airesp):
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    response = combined.lower()

    globals()["isemoting"] = True

    if "forward" in prompt:
        client.send_message("/input/MoveForward", [1])
        time.sleep(2)
        client.send_message("/input/MoveForward", [0])
    if "backward" in prompt:
        client.send_message("/input/MoveBackward", [1])
        time.sleep(2)
        client.send_message("/input/MoveBackward", [0])
    if "left" in prompt:
        client.send_message("/input/LookLeft", [1])
        time.sleep(.45)       
        client.send_message("/input/LookLeft", [0])
    if "right" in prompt and not "alright" in prompt:
        client.send_message("/input/LookRight", [1])
        time.sleep(.45)       
        client.send_message("/input/LookRight", [0])

    if "play" in response and "spotify" in response:
        SpeakText("Sorry, Spotify support isn't currently available.")
    if "play" in response and "youtube" in response:
        SpeakText("Sorry, Youtube support isn't currently available.")
    
    if "follow" in prompt:
        SpeakText("Sorry, the bot cannot currently follow you.")
       
    if "pause" in response and "move" in response:
        globals()["movementpaused"] = True
    else:
        if "unpause" in response and "move" in response:
            globals()["movementpaused"] = False
        else:
            if "moving" in prompt or "move" in prompt and "don't" in prompt or "stop" in prompt or "start" in prompt or "pause" in prompt:
                if globals()["movementpaused"] == False:
                    globals()["movementpaused"] = True
                else:
                    globals()["movementpaused"] = False
        
    
       
          
    globals()["isemoting"] = False

def checkforemotes(response):
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    response = response.lower()
    emote = 0
    globals()["isemoting"] = True
    if "point" in response or "look" in response or "!" in response:
        emote = 3
    if "wave" in response or "hi " in response or "hello" in response:
        emote = 1
    if "clap" in response or "congrat" in response:
        emote = 2
    if "cheer" in response:
        emote = 4
    if "dance" in response:
        emote = 5
    if "backflip" in response or "flip" in response:
        emote = 6
    if "kick" in response:
        emote = 7
    if "die" in response or "dead" in response:
        emote = 8
    if not emote == 0:
        # SENDS DATA TO VRCHAT OVER PARAMS FOCUS, FOCUSLEFT AND FOCUSRIGHT     
        client.send_message("/avatar/parameters/VRCEmote", [int(emote)])
        print("emote # " + str(emote))
        time.sleep(2)
        client.send_message("/avatar/parameters/VRCEmote", [int(0)])      
    globals()["isemoting"] = False


def sendchatbox(aiinput):
    
    messagestring = "%s\v%s" % (globals()["title"], aiinput)
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000) # SENDS DATA TO VRCHAT OVER PARAMS FOCUS, FOCUSLEFT AND FOCUSRIGHT     
    client.send_message("/chatbox/input", [messagestring , True, False])
    if globals()["printtextbox"]:
        print(messagestring)

async def cai():
    #char = "13bcwUru8Qg8BIKBO7NbsHaE3EVeVWlTx4QcV1sG6Oo"
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
            SpeakText("Bot reset. Please try again.")
        else:
            SpeakText("Updated bot. " + answer.text)
            
        
        
        while True:   
            if globals()["botenabled"]:
                try:
                    if globals()["speechrecdone"] == True:
                        globals()["speechrecdone"] = False
                        MyText = globals()["aiinput"]
                        isinputbad = filter(MyText)
                        # isinputbad = False
                        if isinputbad:
                            SpeakText("Prompt is innapropriate. Please try again.")
                        else:
                            sendchatbox("Thinking...\vPrompt: " + globals()["aiinput"])
                            message = await chat.send_message(
                                char, new.chat_id, MyText
                            )
                            
                            isresponsebad = filter(message.text)
                            # isresponsebad = False
                            if isresponsebad:
                                SpeakText("Response is innapropriate. Please try again.")
                            else:
                                print(f'{message.name}: {message.text}')
                                
                                SpeakText(message.text)
                                checkforemotes(message.text + MyText)
                                checkfocommands(message.text + MyText,MyText,message.text)
                                ck = checkforreset(message.text + MyText)
                                if ck:
                                    break
                                globals()["speechrecdone"] = False
                    await asyncio.sleep(0)
                except:
                    globals()["resets"] = globals()["resets"] + 1
                    task2 = asyncio.create_task(cai())
                    await asyncio.gather(task2)
        print("special sauce")
        globals()["resets"] = globals()["resets"] + 1
        task2 = asyncio.create_task(cai())
        await asyncio.gather(task2) 

                
            
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
        globals()["consoleenabled"] = True
        while(True):
            try:
                if globals()["notiflog"]:
                    print("notifications checked!")
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
        if globals()["speechregenabled"]:

            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                
                globals()["listencount"] = globals()["listencount"] + 1
                # Adjust for ambient noise
            

                try:
                    # Capture audio input
                    audio = recognizer.listen(source, timeout=1.5, phrase_time_limit=8)  # Adjust timeout as needed

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
                    if globals()["listencount"] > 7:
                        sendchatbox("Stand in my circle to talk to me!\v(I'm hard of hearing)")
                        globals()["listencount"] = 0
                except sr.UnknownValueError:
                    print("Speech recognition could not understand audio.")
                    
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                
                    
                
        

def move():  
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    while (True):
            
        if globals()["speechrecdone"] == False and globals()["isemoting"] == False and globals()["movementpaused"] == False:
            time.sleep(2.6)
            num = random.randrange(1, 8)
            if globals()["printnumgen"]:
                print(num)
                
            if num == 1:
                client.send_message("/input/Jump", [1])
                num2 = random.randrange(1,2)
                #print("jump for " + str(num2) + " seconds")
                client.send_message("/input/Jump", [0])
                
            if num == 6:
                client.send_message("/input/MoveForward", [1])
                num2 = random.randrange(1,2)
                #print("moving forward for " + str(num2) + " seconds")
                time.sleep(num2)
                client.send_message("/input/MoveForward", [0])

            if num == 4:
                client.send_message("/input/LookLeft", [1])
                num2 = random.randrange(10, 75)
                num3 = num2 / 100
                #print("left for " + str(num3) + " seconds")
                time.sleep(num3)
                client.send_message("/input/LookLeft", [0])

            if num == 2:
                client.send_message("/input/LookRight", [1])
                num2 = random.randrange(10, 75)
                num3 = num2 / 100
                #print("right for " + str(num3) + " seconds")
                time.sleep(num3)
                client.send_message("/input/LookRight", [0])
                

def console():
    while True:
        if globals()["consoleenabled"] == True:
            text = input()
            if "#" in text: #to talk to the bot
                globals()["aiinput"] = text
                globals()["speechrecdone"] = True
            else:
                globals()["title"] = "||Message from Creator||"
                if not "/" in text: #to run commands without the bot speaking it
                    SpeakText(text)
                checkforreset(text)
                checkfocommands(text, text, text)
                checkforemotes(text)
                debugcommandscheck(text)
                globals()["title"] = "🐝Tigerbee Bot🐝"



            



def SpeakText(command):
    try:
        globals()["listencount"] = 0
        sendchatbox(command)
            # Initialize mixer with the correct device
        # Set the parameter devicename to use the VB-CABLE name from the outputs printed previously.
        mixer.init(devicename = "CABLE Input (VB-Audio Virtual Cable)")
    
        tts = gTTS(command.replace(":", " colon "), lang='en')
        tts.save(str(globals()["num"]) + ".mp3")
        audio = AudioSegment.from_file(str(globals()["num"]) + ".mp3")

        # Apply speed up factor
        audio = audio.speedup(playback_speed=1.2)

        # Export modified audio
        audio.export(str(globals()["num"]) + "sped.mp3", format="mp3")
        # Play the saved audio file
        mixer.music.load(str(globals()["num"]) + "sped.mp3")
        mixer.music.play()
        mixer.stop()
        globals()["num"] += 1
    except:
        sendchatbox("Text to speech has failed. Please contact the owner of this bot.")
    

        
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
    thread4 = threading.Thread(target=console)
    thread4.start()

    # Let tasks run indefinitely without waiting for them to complete
    await asyncio.gather(task2)

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())