import os
from google.cloud import speech
from googletrans import Translator
from pydub import AudioSegment
from pydub.utils import mediainfo

# Set Google credentials path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

# Convert .wav to .flac
def convert_audio_to_flac(input_path):
    audio = AudioSegment.from_file(input_path)
    flac_path = input_path.replace(".wav", ".flac")
    audio.export(flac_path, format="flac")
    return flac_path

# Transcribe speech
from pydub.utils import mediainfo

def transcribe_audio(path):
    client = speech.SpeechClient()

    with open(path, "rb") as audio_file:
        content = audio_file.read()

    # Automatically detect sample rate
    info = mediainfo(path)
    actual_sample_rate = int(info['sample_rate'])

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=actual_sample_rate,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "
    return transcript.strip()

# Translate speech
def translate_text(text, target_lang="fr"):
    translator = Translator()
    translated = translator.translate(text, dest=target_lang)
    return translated.text

# Run both
def transcribe_and_translate(audio_path, target_lang="fr"):
    flac_path = convert_audio_to_flac(audio_path)
    transcript = transcribe_audio(flac_path)
    translated = translate_text(transcript, target_lang)
    return {"original": transcript, "translated": translated}

# Test
if __name__ == "__main__":
    result = transcribe_and_translate("Sample-audio.mp3", "hi")  # Hindi
    print(result)