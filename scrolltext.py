from mutagen.mp3 import MP3
import syllables
stop_event = threading.Event()
message_thread = None
is_talking = False
mp3Length = 0

def SpeakText(command):
    try:
        global lang
        global mp3Length
        global is_talking
        global stop_event
        global message_thread

        if message_thread and message_thread.is_alive():
            stop_event.set()
            message_thread.join() # waits till last chunk is done
        stop_event = threading.Event()
        is_talking = False

        # Initialize mixer with the correct device
        # Set the parameter devicename to use the VB-CABLE name from the outputs printed previously.
        mixer.init(devicename = "CABLE Input (VB-Audio Virtual Cable)", frequency=48510)

        tts = gTTS(command.replace(":", " colon "), lang=lang)
        tts.save(str(globals()["num"]) + ".mp3")
        audio = AudioSegment.from_file(str(globals()["num"]) + ".mp3")

        # Apply speed up factor
        audio = audio.speedup(playback_speed=1.2)

        # Export modified audio
        audio.export(str(globals()["num"]) + "sped.mp3", format="mp3")

        # Checking mp3 length
        audio_temp = MP3(str(num) + "sped.mp3")
        mp3Length = audio_temp.info.length
        #print(mp3Length)


        def monitor_audio_playback(mp3Length):
            global is_talking
            is_talking = True
            #print("is_talking TRUE")

            start_time = time.time()

            while time.time() - start_time < mp3Length:
                if stop_event.is_set():
                    print("Playback interrupted.")
                    is_talking = False
                    return
                time.sleep(0.1)

            is_talking = False
            #print("is_talking FALSE")

        # Start a thread for is_talking, used for blocking idle message
        audio_thread = threading.Thread(target=monitor_audio_playback, args=(mp3Length,))
        audio_thread.start()


        try:
            mixer.music.load(str(globals()["num"]) + "sped.mp3")
            mixer.music.play()
            mixer.stop()
            globals()["num"] += 1
        except Exception as e:
            print(f"SpeakText error: {e}")

        # Chunking the input to 126 characters and saving in list
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
                delay = syllable_count * 0.23  #0.23 seconds per syllable
                sendchatbox(chunk)
                time.sleep(delay)

        message_thread = threading.Thread(target=send_chunks_with_delay, args=(chunks,))
        message_thread.start()

    except Exception as e:
        print(f"General error: {e}")
        sendchatbox("Text to speech has failed.")