[![](https://img.shields.io/github/license/tuckerisapizza/VRChat-AI-Bot)](LICENSE) [![](https://img.shields.io/discord/1251927684313776219?label=Discord&logo=discord)](https://discord.com/invite/YdKaGRQ7th)

# VRChat-AI-Bot

My attempt at making a VRChat AI bot. I'd say the result is extremely good.
Runs on practically any hardware, including integrated graphics, as long as the hardware can run VRChat desktop with at least 15 FPS. This is a result of all processing done remotely.

 - **Character AI**: custom chatbots and conversations
 - **Google STT and TTS**: allows hearing and vocal responses.

*Wanting a different AI model to use?* Check out some of the other branches [here](https://github.com/tuckerisapizza/VRChat-AI-Bot/branches)!

### Setup

1. It is recommended to install the repository via the latest release [here](https://github.com/tuckerisapizza/VRChat-AI-Bot/releases/latest), but if you want newly-introduced features you can download the latest commit [here](https://github.com/tuckerisapizza/VRChat-AI-Bot/archive/refs/heads/main.zip).
2. Install the dependencies by running `pip install -r requirements.txt` in a terminal which is opened to the repository. You can do so by running `cd <DIRECTORY>`.
3. You'll need to get your CharacterAI key. Follow the guide [here](https://docs.kram.cat/auth.html); input your email, then the link from the email they send you.
4. In the `credentials.py` file, change all the necessary values to yours. This is where you'll put your CharacterAI key. **Do not commit or push any changes from this file!**
5. Download your virtual audio cables. Software from [VB-Audio](https://vb-audio.com/Cable/index.htm) is really good, with the recommended software being [Voicemeeter Banana](https://vb-audio.com/Voicemeeter/banana.htm). However, any software works as long as you can route **2** virtual audio cables.
6. Route one VAC from the **script's output** to **VRChat's input**; this is for the bot's speech. Route the other VAC from the **script's input** to **VRChat's output**; this is for the bot's hearing.
7. Once everything is set up, you can run the program via `python botscript_torelease.py`.

### License

This project is licensed under the [MIT License](https://opensource.org/license/mit), which can be found [here](./License).

TL;DR, preserve the copyright and license notices for your changes.
