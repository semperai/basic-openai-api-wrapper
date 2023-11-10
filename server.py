import torch
import json
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from faster_whisper import WhisperModel
from TTS.api import TTS

whisper_model = "tiny.en"

# uncomment this to make higher quality, but slower
# whisper_model = "base.en"

# you can change this if using gpu
# int8 is better for m1 cpu
whisper_compute_type = "int8"

tts_multilingual = False # set to true if using xtts_v2

tts_model = "tts_models/en/ljspeech/vits"
# print(TTS().list_models()) # in case you want to see all options

# uncomment this to make higher quality but slower
# you can replace speaker.wav with your own audio file
# tts_model = "tts_models/multilingual/multi-dataset/xtts_v2"

whisper = WhisperModel(
    whisper_model,
    device="auto",
    compute_type=whisper_compute_type
)

tts = TTS(tts_model).to("cuda" if torch.cuda.is_available() else "cpu")

app = Flask(__name__)
CORS(app)

@app.route('/v1/audio/transcriptions', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return 'No file part', 400

    f = request.files["file"]
    f.save("input.wav")

    segments, info = whisper.transcribe("input.wav", beam_size=5)

    print(info)
    print(segments)

    text = ""
    for segment in segments:
        text += segment.text
    return json.dumps({"text": text})

@app.route('/v1/audio/speech', methods=['POST'])
def speech():
    content = request.json
    if "model" not in content:
        return 'No model specified', 400
    if "input" not in content:
        return 'No input specified', 400
    if "voice" not in content:
        return 'No voice specified', 400

    if tts_multilingual:
        tts.tts_to_file(
            text=content["input"],
            speaker_wav="speaker.wav",
            language="en",
            file_path="ttsoutput.wav"
        )
    else:
        tts.tts_to_file(
            text=content["input"],
            speaker_wav="speaker.wav",
            file_path="ttsoutput.wav"
        )


    return send_from_directory(
        directory=".",
        path="ttsoutput.wav",
        as_attachment=True
    )

app.run()
