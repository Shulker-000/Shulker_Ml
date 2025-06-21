from flask import Blueprint, request, jsonify
from .utils import translator
import os

bp = Blueprint('api', __name__)

# Load Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

@bp.route('/translate-audio', methods=['POST'])
def translate_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    filename = "temp_audio.wav"
    file.save(filename)

    try:
        translated_text = translator.transcribe_and_translate(filename, target_lang="hi")
        return jsonify({"caption": translated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500