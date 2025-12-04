import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

# Configure translation: recognize Hindi (hi-IN), output English (en)
translation_config = speechsdk.translation.SpeechTranslationConfig(
    endpoint=os.getenv("AZURE_SPEECH_SERIVCE_ENDPOINT", ""),
    subscription=os.getenv("AZURE_SPEECH_SERIVCE_KEY", ""),
    region=os.getenv("AZURE_SPEECH_REGION", ""),
)
translation_config.speech_recognition_language = "hi-IN"
translation_config.add_target_language("en")
translation_config.voice_name = "en-US-JennyNeural"  # cqhoose any English neural voice

# Use the default microphone as audio input
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

# Create the recognizer for translation
translator = speechsdk.translation.TranslationRecognizer(
    translation_config=translation_config, audio_config=audio_config
)

print("Start speaking...")


# Continuously listen and translate
def handle_result(evt):
    # evt.result.translations is a dict keyed by target language
    english = evt.result.translations.get("en", "")
    if english:
        print(f"Transcribed: {evt.result.text}")
        print(f"Translated: {english}\n")


# Attach callbacks for partial and final results
translator.recognizing.connect(lambda evt: handle_result(evt))
translator.recognized.connect(lambda evt: handle_result(evt))

# Start continuous recognition. This call is non-blocking.
translator.start_continuous_recognition()

try:
    # Keep the script running, or integrate into your GUI/event loop
    while True:
        pass
except KeyboardInterrupt:
    translator.stop_continuous_recognition()
