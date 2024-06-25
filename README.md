# VRChat-AI-Bot

My attempt at making a VRChat AI bot. I'd say the result is extremely good.
Runs on practically any hardware, including integrated graphics.
As long as the hardware can run VRChat desktop at atleast 15 fps.
This is a result of all processing done remotely.

The branch utilizes OLLaMA for custom AI models, Google Speech to text, and Google Text to speech.

# README

download both botscript.py and credentials.py and put them both in the same folder

i recommend you setup your audio pipelines before you even go installing packages

speaker needs to be mapped to microphone using VB-Audio Cable (for text to speech)

microphone needs to be mapped to speaker using a physical aux cable connecting a speaker output to microphone input (for speech recognition)

then, install packages and replace neccessary values such as your VRChat login and ollama model

input your vrchat credentials and custom user agent into credentials.py

after that, test if it works by playing a youtube video and see if the script detects the youtube video's audio and the bot responds to it
good luck!
