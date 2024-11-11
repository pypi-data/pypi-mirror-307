import requests
import json
import sys
from unidecode import unidecode

def translate_text(text, input_lang='auto', output_lang='en'):
    if len(text) <= 4000:
        # Request URL...
        GOOGLE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"
        """Translates given text using the Google Translate API."""
        params = {
            'client': 'gtx',
            'sl': input_lang,
            'tl': output_lang,
            'dt': 't',
            'q': text,
        }
        response = requests.get(GOOGLE_TRANSLATE_URL, params=params)
        result = response.json()
        translated_text = ''.join([item[0] for item in result[0]])
        if response.status_code != 'Error' or '443' not in unidecode(translated_text):
            return json.dumps({'RESPONSE_STATUS': response.status_code,'TranslatedText': unidecode(translated_text)})
        else:
            return json.dumps({'RESPONSE_STATUS': 500,'TranslatedText': "Something went wrong please pass proper text..."})
    else:
        return json.dumps({'RESPONSE_STATUS': 200, 'Message': "More than 4000 Character not Allowed..."})

print(translate_text("How are you?","en","es"))