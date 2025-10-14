"""
Speech Synthesis MarkUP Language Example
"""

import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

speech_config = speechsdk.SpeechConfig(
    endpoint=os.getenv("AZURE_SPEECH_SERIVCE_ENDPOINT", ""),
    subscription=os.getenv("AZURE_SPEECH_SERIVCE_KEY", ""),
)

ssml_string = """
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
  <voice name="en-US-JennyNeural">
    Hello there! Welcome to Azure Speech Service.
  </voice>
</speak>
"""

output_file = "outputs/ssml_speech01.wav"
audio_config = speechsdk.audio.AudioConfig(filename=output_file)

speech_generator = speechsdk.SpeechSynthesizer(
    speech_config=speech_config, audio_config=audio_config
)

result = speech_generator.speak_ssml_async(ssml_string).get()

if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Successfully genereted speech")
else:
    print("Something went wrong")
