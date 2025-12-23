import speech_recognition as sr

def speech_to_text_push_to_talk():
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True

    input(" మైక్ ఆన్ చేయడానికి ENTER నొక్కండి...")
    print(" మాట్లాడండి... (మాట్లాడిన తర్వాత ENTER నొక్కండి)")

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    input(" మైక్ ఆఫ్ చేయడానికి ENTER నొక్కండి...")

    try:
        text = r.recognize_google(audio, language="te-IN")
        return text.strip()
    except:
        return ""
