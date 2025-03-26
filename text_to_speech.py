'''
  For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk
'''

import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def synthesize_speech(text: str, voice_name: str = "en-IE-EmilyNeural", region: str = "swedencentral"):
    """
    Synthesizes speech from the given text using Azure Cognitive Services.

    Args:
        text (str): The text to synthesize.
        voice_name (str): The voice to use for synthesis (default is "en-IE-EmilyNeural").
        region (str): The Azure region for the speech service (default is "swedencentral").

    Returns:
        None
    """
    # Get the speech key from environment variables
    speech_key = os.environ.get("AI_KEY")
    if not speech_key:
        raise ValueError("SPEECH_KEY environment variable is not set.")

    # Create an instance of a speech config with the specified subscription key and service region
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    speech_config.speech_synthesis_voice_name = voice_name

    # Use the default speaker as audio output
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Perform speech synthesis
    result = speech_synthesizer.speak_text_async(text).get()

    # Check the result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text: {text}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

# Example usage
# text = "Hi, this is Emily. Do you like my Irish accent?"
# synthesize_speech(text)
