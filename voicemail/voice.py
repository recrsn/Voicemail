import speech_recognition as sr
import pyttsx3
import tempfile
import os
from google.cloud import texttospeech
# from playsound import playsound
import subprocess


class TTSEngine:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US', ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
        self.audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    def speak(self, text):
        print('>>>', text)
        synthesis_input = texttospeech.types.SynthesisInput(text=text)
        response = self.client.synthesize_speech(
            synthesis_input, self.voice, self.audio_config)

        with tempfile.NamedTemporaryFile(suffix=".mp3") as f:
            f.write(response.audio_content)
            # playsound(f.name)
            subprocess.call(["ffplay", '-nodisp', '-autoexit', '-i', f.name],
                            stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL)


def text_to_speech(sentence):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(sentence)
    engine.runAndWait()
    del engine


def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    while True:
        try:
            # Speech recognition using Google Speech Recognition
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            # with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS']) as f:
            text = r.recognize_google(audio)
            print("You said: " + text)
            return text

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")