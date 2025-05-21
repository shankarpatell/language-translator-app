from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)


HF_TOKEN = "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"  

def translate_huggingface(text, src_lang, tgt_lang):
    
    
    model_map = {
        ('en', 'fr'): 'Helsinki-NLP/opus-mt-en-fr',
        ('en', 'de'): 'Helsinki-NLP/opus-mt-en-de',
        ('en', 'es'): 'Helsinki-NLP/opus-mt-en-es',
        ('fr', 'en'): 'Helsinki-NLP/opus-mt-fr-en',
        ('de', 'en'): 'Helsinki-NLP/opus-mt-de-en',
        ('es', 'en'): 'Helsinki-NLP/opus-mt-es-en',
    }

    model = model_map.get((src_lang, tgt_lang))
    if not model:
        return f"❌ Translation from {src_lang} to {tgt_lang} is not supported."

    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = { "inputs": text }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and 'translation_text' in result[0]:
            return result[0]['translation_text']
        else:
            return f"⚠️ Unexpected response format: {result}"
    except requests.exceptions.RequestException as e:
        return f"❌ Request error: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text')
    src_lang = data.get('src_lang')
    tgt_lang = data.get('dest_lang')

    translated = translate_huggingface(text, src_lang, tgt_lang)
    return jsonify({'translated_text': translated})

if __name__ == '__main__':
    app.run(debug=True)
