from gtts import gTTS
import os
import time

def speak(text):
    try:
        tts = gTTS(text=text, lang="te")
        tts.save("output.mp3")

        # Windows లో mp3 play చేసి పూర్తయ్యేవరకు wait
        os.system("start /wait output.mp3")

        time.sleep(0.5)
    except Exception as e:
        print(" Telugu TTS failed (check internet):", e)
