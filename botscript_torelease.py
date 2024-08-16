from concurrent.futures import ThreadPoolExecutor
from functools import cache
from characterai import pycai
import speech_recognition as sr
from gtts import gTTS
from pygame import mixer, _sdl2 as devices
from pythonosc import udp_client
import vrchatapi
from vrchatapi.api import authentication_api, notifications_api, groups_api
from vrchatapi.exceptions import UnauthorizedException
from vrchatapi.models.two_factor_auth_code import TwoFactorAuthCode
from vrchatapi.models.two_factor_email_code import TwoFactorEmailCode
from vrchatapi.models.create_group_invite_request import CreateGroupInviteRequest
from pydub import AudioSegment
import threading
import random
import time
import credentials
from mutagen.mp3 import MP3
import syllables

stop_event = threading.Event()
message_thread = None
is_talking = False
mp3Length = 0

resets = 0 #keeps track of if the bot breaks and restarts it
bottitle = "🐝Tigerbee Bot🐝" # the bots title used in chatboxes
listencount = 0 #keeps track of how many times the bot has gone without a prompt
isemoting = False
movementpaused = False
consoleenabled = False
num = 0

#debug variables
printnumgen = False
printtextbox = True
botenabled = True
speechregenabled = True
notiflog = False

def mainthread():
    global resets, listencount
    
    char = credentials.CAI_CHARACTER
    client = pycai.Client(credentials.CAI_API_KEY)
    me = client.get_me()
    with client.connect() as chat:
        new, answer = chat.new_chat(
            char, me.id
        )
        print(f'{answer.name}: {answer.text}')
        if resets > 0:
            SpeakText("Bot reset. Please try again.")
        else:
            SpeakText("Updated bot. " + answer.text)
        sendchatbox("Initializing Speech Recognition...")
        while(True):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                listencount = listencount + 1
                # Adjust for ambient noise
                try:
                    # Capture audio input
                    audio = recognizer.listen(source, timeout=1.5, phrase_time_limit=8)  # Adjust timeout as needed
                    print("Recognizing...")
                    # Use Google Speech Recognition
                    sentence = recognizer.recognize_google(audio)
                    # Print recognized sentence
                    print(f"Recognized: {sentence}")
                    text = sentence
                    if filter(text):
                        print(f'BAD WORD FOUND in prompt "{text}"')
                        SpeakText("Prompt is innapropriate. Please try again.")
                    else:
                        
                        sendchatbox("Thinking...\vPrompt: " + text)
                        message = chat.send_message(
                             char, new.chat_id, text
                        )
                        if filter(message.text):
                            print(f'BAD WORD FOUND in response "{message.text}"')
                            SpeakText("Response is innapropriate. Please try again.")
                        else:
                            listencount = 0
                            print(f'{message.name}: {message.text}')
                            if checkforreset(message.text + text):
                                break
                            SpeakText(message.text)
                            checkforemotes(message.text + text)
                            checkforcommands(message.text + text,text)
                        
                except sr.WaitTimeoutError:
                    if listencount > 12:
                        sendchatbox("Stand in my circle to talk to me!\v(I'm hard of hearing)")
                        listencount = 0
                except sr.UnknownValueError:
                    print("Speech recognition could not understand audio.")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")

def move():  
    global isemoting, movementpaused, printnumgen
    
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    while (True):
        if isemoting == False and movementpaused == False:
            time.sleep(2.6)
            num = random.randrange(1, 8)
            if printnumgen:
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
    global consoleenabled, bottitle
    
    while True:
        if consoleenabled == True:
            text = input()
            bottitle = "||Message from Creator||"
            if not "/" in text: #to run commands without the bot speaking it
                SpeakText(text)
            checkforreset(text)
            checkforcommands(text, text)
            checkforemotes(text)
            debugcommandscheck(text)
            bottitle = "🐝Tigerbee Bot🐝"

def checkinvites():
    global consoleenabled, notiflog
    
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
        consoleenabled = True
        while(True):
            try:
                if notiflog:
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

def SpeakText(command):
    try:
        global mp3Length
        global is_talking
        global stop_event
        global message_thread
        global num
        
        mixer.init(devicename = "CABLE Input (VB-Audio Virtual Cable)")
        sendchatbox("Generating Text to Speech...")
        # Stop any existing playback or message thread
        if message_thread and message_thread.is_alive():
            stop_event.set()
            message_thread.join()  # Waits till the last chunk is done
        stop_event = threading.Event()
        is_talking = False


        # Create and save TTS output
        tts = gTTS(command.replace(":", " colon "), lang='en')
        tts_filename = f"{num}.mp3"
        tts.save(f"{num}norm.mp3")
        
        audio = AudioSegment.from_file(str(num) + "norm.mp3")
        # Apply speed up factor
        audio = audio.speedup(playback_speed=1.2)
        # Export modified audio
        audio.export(str(num) + ".mp3", format="mp3")

        # Check MP3 length
        audio_temp = MP3(tts_filename)
        mp3Length = audio_temp.info.length

        # Monitor audio playback
        def monitor_audio_playback(mp3Length):
            global is_talking
            is_talking = True
            start_time = time.time()

            while time.time() - start_time < mp3Length:
                if stop_event.is_set():
                    print("Playback interrupted.")
                    is_talking = False
                    return
                time.sleep(0.1)

            is_talking = False

        # Start a thread for is_talking
        audio_thread = threading.Thread(target=monitor_audio_playback, args=(mp3Length,))
        audio_thread.start()

        try:
            
            mixer.music.load(tts_filename)
            mixer.music.play()

            # Increment the global num counter
            num += 1

            # Schedule file deletion after playback
            

        except Exception as e:
            print(f"SpeakText error: {e}")

        # Chunk the input for sending
        chunks = []
        start = 0
        while start < len(command):
            end = min(start + 126, len(command))
            if end < len(command) and command[end] != ' ':
                end = command.rfind(' ', start, end)
                if end == -1 or end <= start:
                    end = start + 126

            chunk = command[start:end].strip()
            chunks.append(chunk)
            start = end

        print("Chunks:", chunks)

        # Start sending the chunks in a separate thread
        def send_chunks_with_delay(chunks):
            for chunk in chunks:
                if stop_event.is_set():
                    print("Stopping message sending thread.")
                    break
                syllable_count = sum(syllables.estimate(word) for word in chunk.split())
                delay = syllable_count * 0.23  # 0.23 seconds per syllable
                sendchatbox(chunk)
                time.sleep(delay)

        message_thread = threading.Thread(target=send_chunks_with_delay, args=(chunks,))
        message_thread.start()

    except Exception as e:
        print(f"General error: {e}")
        sendchatbox("Text to speech has failed. Please contact the owner of this bot.\v" + Exception)

def sendchatbox(aiinput):
    global bottitle, printtextbox
    
    messagestring = "%s\v%s" % (bottitle, aiinput)
    if len(messagestring) > 144:
        messagestring = messagestring[:140] + "..."
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000) 
    client.send_message("/chatbox/input", [messagestring, True, False])
    if printtextbox:
        print(messagestring)

@cache
def filterlist() -> set[str]:
    with open("filtered-list.txt", "r") as file:
        return set(line.strip().lower() for line in file if line.strip())

def filter(input: str) -> bool:
    input_lower = input.lower()
    return any(item in input_lower for item in filterlist())    

def checkforreset(text):
    response = text.lower()
    if (("reset" in response or "restart" in response) and ("box" in response or "bot" in response or "bbott" in response or "Bebop" in response or "butt" in response)):
        return True
    else:
        return False
    
def checkforcommands(combined: str, prompt: str) -> None:
    global isemoting, movementpaused

    client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    response = combined.lower()
    isemoting = True

    futures = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        def command(address: str, sleep: float) -> None:
            print(address, 1)
            client.send_message(address, [1])
            time.sleep(sleep)
            print(address, 0)
            client.send_message(address, [0])

        if "forward" in prompt:
            futures.append(executor.submit(command, "/input/MoveForward", 2.0))
        if "backward" in prompt:
            futures.append(executor.submit(command, "/input/MoveBackward", 2.0))
        if "left" in prompt:
            futures.append(executor.submit(command, "/input/LookLeft", 0.45))
        if "right" in prompt and "alright" not in prompt:
            futures.append(executor.submit(command, "/input/LookRight", 0.45))

    if "play" in response and "spotify" in response:
        SpeakText("Sorry, Spotify support isn't currently available.")
    if "play" in response and "youtube" in response:
        SpeakText("Sorry, Youtube support isn't currently available.")
    if "follow" in prompt:
        SpeakText("Sorry, the bot cannot currently follow you.")

    if "pause" in response and "move" in response:
        movementpaused = True
    elif "unpause" in response and "move" in response:
        movementpaused = False

    if (
        "moving" in prompt
        or "move" in prompt
        and "don't" in prompt
        or "stop" in prompt
        or "start" in prompt
        or "pause" in prompt
    ):
        movementpaused = not movementpaused
    isemoting = False

    for future in futures:
        future.result()

def checkforemotes(response):
    global isemoting
    
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    response = response.lower()
    emote = 0
    isemoting = True
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
        client.send_message("/avatar/parameters/VRCEmote", [int(emote)])
        print("emote # " + str(emote))
        time.sleep(2)
        client.send_message("/avatar/parameters/VRCEmote", [int(0)])      
    isemoting = False

def debugcommandscheck(text):
    global printnumgen, botenabled, printtextbox, speechregenabled, notiflog, movementpaused, speechrecdone
    
    if "printnumgen" in text:
        if printnumgen:
            printnumgen = False
        else:
            printnumgen = True
        print(printnumgen)

    if "botenabled" in text:
        if botenabled:
            botenabled = False
        else:
            botenabled = True
        print(botenabled)

    if "printtextbox" in text:
        if printtextbox:
            printtextbox = False
        else:
            printtextbox = True
        print(printtextbox)

    if "speechregenabled" in text:
        if speechregenabled:
            speechregenabled = False
        else:
            speechregenabled = True
        print(speechregenabled)

    if "notiflog" in text:
        if notiflog:
            notiflog = False
        else:
            notiflog = True
        print(notiflog)

    if "movement" in text:
        if movementpaused:
            movementpaused = False
        else:
            movementpaused = True
        print(movementpaused)

    if "speechrecdone" in text:
        if speechrecdone:
            speechrecdone = False
        else:
            speechrecdone = True
        print(speechrecdone)
        
def main():
    global resets
    
    mixer.init()
    print("Outputs:", devices.audio.get_audio_device_names(False))
    mixer.quit()
    # Initialize the recognizer 
    r = sr.Recognizer()
    thread2 = threading.Thread(target=checkinvites)
    thread2.start()
    thread3 = threading.Thread(target=move)
    thread3.start()
    thread4 = threading.Thread(target=console)
    thread4.start()
    
    while True:
        mainthread()
        resets = resets + 1

if __name__ == "__main__":
    main()    
