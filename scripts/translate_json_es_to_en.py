from .translate_text import translate_with_deepl
from .process_json import load_json, write_json


def translate_transcription(file_path):
    """
    Translates transcription from Spanish to English.
    """
    data = load_json(file_path)
    utterances = data.get('utterances', [])

    for utterance in utterances:
        original_text = utterance['text']
        if 'text_en' in utterance and utterance['text_en'] != "" : return
        else: 
            translated_text = translate_with_deepl(original_text)
            utterance['text_en'] = translated_text
    data['utterances'] = utterances
    # Update the original JSON file with translations
    write_json(data, file_path)
    print(f"Translated utterances updated in {file_path}")