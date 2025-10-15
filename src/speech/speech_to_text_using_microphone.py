import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

speech_config = speechsdk.SpeechConfig(
    endpoint=os.getenv("AZURE_SPEECH_SERIVCE_ENDPOINT", ""),
    subscription=os.getenv("AZURE_SPEECH_SERIVCE_KEY", ""),
)
speech_config.speech_recognition_language = "en-US"

output_file = "outputs/transcribed.txt"
# audio_file = "outputs/speech01.wav"

audio_input = speechsdk.audio.AudioConfig(use_default_microphone=True)

speech_generator = speechsdk.SpeechRecognizer(
    speech_config=speech_config, audio_config=audio_input
)

result = speech_generator.recognize_once_async().get()

if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Text generated Successfully.")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(result.text)
else:
    print("Something went wrong!")
