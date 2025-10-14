import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

speech_config = speechsdk.SpeechConfig(
    endpoint=os.getenv("AZURE_SPEECH_SERIVCE_ENDPOINT", ""),
    subscription=os.getenv("AZURE_SPEECH_SERIVCE_KEY", ""),
)
speech_config.speech_synthesis_voice_name = "en-US-SteffanMultilingualNeural"

input_txt = "Hello there! How are you? Myself Dhruv, i am passionate software engineer working at Presidio. I provide AI services in many domains such as E-Commerce, Education, Cloud Automation. You can explore my website to see offered services and contact details"

output_file = "outputs/speech01.wav"

audio_config = speechsdk.audio.AudioConfig(filename=output_file)

speech_generator = speechsdk.SpeechSynthesizer(
    speech_config=speech_config, audio_config=audio_config
)

result = speech_generator.speak_text_async(input_txt).get()

if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech Audio generated Successfully.")
else:
    print("Something went wrong!")
