import speech_recognition as sr

def recognize_speech(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        text = "Sorry, I didn't catch that."
    except sr.RequestError:
        text = "Sorry, there was an issue with the request."
    return text
