import speech_recognition as sr

def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 మాట్లాడండి...")
        audio = r.listen(source)
    return audio
