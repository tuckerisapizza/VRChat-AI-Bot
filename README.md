# VRChat-AI-Bot **WORK IN PROGRESS HUGGINGCHAT BRANCH**

My attempt at making a VRChat AI bot. I'd say the result is extremely good.
Runs on practically any hardware, including integrated graphics, as long as the hardware can run VRChat desktop with at least 15 FPS. This is a result of all processing done remotely.

 - **Hugging Chat**: custom chatbots with system prompts, ai tools, many more features than CharacterAI
 - **Google STT and TTS**: allows hearing and vocal responses.

### Setup

Pre-requisite: Make sure between Python 3.6-3.11 is installed, otherwise HuggingChat will not work :/
1. Download the latest release [here](https://github.com/tuckerisapizza/VRChat-AI-Bot/releases/latest) or the latest commit [here](https://github.com/tuckerisapizza/VRChat-AI-Bot/archive/refs/heads/main.zip).
2. Install the dependencies by running `pip install -r requirements.txt` in a terminal which is opened to the repository. You can do so by running `cd <DIRECTORY>`.
3. In the `credentials.py` file, change all the necessary values to yours. This is where you'll put your system prompt, VRChat login, and your HuggingFace login.
4. Download your virtual audio cables. Any software from [VB-Audio](https://vb-audio.com/Cable/index.htm) is really good, with the recommended software being [Voicemeeter Banana](https://vb-audio.com/Voicemeeter/banana.htm). Make sure you choose a software that allows you to route **2** virtual inputs and outputs.
5. Route one VAC the script's output to VRChat's input; this is for the bot's speech. Route the other VAC the script's input to VRChat's output; this is for the bot's hearing.

### License

This project is licensed under the MIT License, which can be found [here](./License).

TL;DR, preserve the copyright and license notices for your changes.
