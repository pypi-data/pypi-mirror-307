# sdTranslate

`sdTranslate` is a lightweight Python package that uses Google Translate API to translate text from one language to another. With a straightforward interface, it supports auto-detection of the input language and provides results in JSON format.

## Installation

Clone or download the repository, and install the dependencies.

```bash
pip install sdTranslate
```

## Usage
Import the translate_text function from sdTranslate and provide the text you want to translate, with optional parameters for input and output languages.

```bash
from sdTranslate import translate_text

# Example usage
result = translate_text("Hola, ¿cómo estás?", input_lang="es", output_lang="en")
print(result)
```

## Function Signature
```bash
translate_text(text, input_lang='auto', output_lang='en')
```

- text: str - The text to be translated. Limited to 4000 characters.
- input_lang: str - Language code for the input text (default is 'auto' for auto-detection).
- output_lang: str - Language code for the output text (default is 'en' for English).

## Example Response
The translate_text function returns a JSON string with the following structure:

```bash
{
  "RESPONSE_STATUS": 200,
  "TranslatedText": "How are you?"
}

```

If there’s an error in the translation or an invalid text input:

```bash
{
  "RESPONSE_STATUS": 500,
  "TranslatedText": "Something went wrong please pass proper text..."
}
```

## Dependencies
- requests: For making HTTP requests to the Google Translate API.
- unidecode: For converting the translated text into plain ASCII characters.

## License
This project is licensed under the MIT License.

```bash

This `README.md` provides clear instructions on using the `translate_text` function, including details about parameters, expected output, and error handling. It should help users understand and get started with your package quickly.

```