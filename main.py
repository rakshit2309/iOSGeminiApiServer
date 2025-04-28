from flask import Flask, request, jsonify
import google.generativeai as genai
import base64

from dotenv import load_dotenv
import requests 
import os


load_dotenv()

app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro')






@app.route('/analyze_audio', methods=['POST'])
def analyze_audio():
    try:
        data = request.get_json()
        audio_base64 = data['audio_base64']
        text_prompt = data['text_prompt']

        audio_data = base64.b64decode(audio_base64)

        contents = {
            "parts": [
                {"mime_type": "audio/wav", "data": audio_data},
                {"text": text_prompt},
            ],
        }

        response = model.generate_content(contents)
        return jsonify({'result': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

