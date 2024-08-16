# VRChat-AI-Bot

## Overview
Welcome to **VRChat-AI-Bot**, my personal endeavor in creating a VRChat AI bot. The results have been impressive, with the bot running on nearly any hardware that can handle VRChat desktop at a minimum of 15 FPS. This is made possible by performing all the processing remotely.

The bot leverages the power of **Character AI** for custom AI chatbots, **Google Speech-to-Text**, and **Google Text-to-Speech** to create an engaging experience.

### Important Note
Check out our different branches for other AI model architectures. The `main` branch focuses on Character AI.

---

## Getting Started

### 1. Download Required Files
To get started, download the following files and place them in the same directory:
- `botscript.py`
- `credentials.py`
- `requirements.txt`

### 2. Set Up Audio Pipelines
Before installing any packages, ensure that your audio pipelines are properly set up:

- **Text-to-Speech:** Use **VB-Audio Cable** to map your speaker output to the microphone input.
- **Speech Recognition:** Connect a speaker output to the microphone input using a physical aux cable.

### 3. Install Dependencies
Once your audio pipelines are configured, install the necessary packages using `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configure Credentials
#### Character AI
- Obtain your Character AI API key by following [this guide](https://docs.kram.cat/auth.html). Run the script on the page, input the link they email you, and use the key in `credentials.py`.
- Input a Character AI character into `credentials.py`.

#### VRChat
- Input your VRChat credentials and custom user agent into `credentials.py`.

### 5. Testing
To verify that everything is set up correctly, play a YouTube video. The script should detect the video's audio, and the bot should respond accordingly.

---

## Additional Information

### Dependencies
- **Character AI**
- **VB-Audio Cable** for audio routing

### Contributing
Feel free to fork this repository and submit pull requests if you have any improvements or new features you'd like to add.

### License
This project is licensed under the MIT License - see the `LICENSE` file for details.

Good luck, and have fun building your VRChat AI bot!
