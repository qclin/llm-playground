from .translate_text import translate_with_deepl
from .process_json import load_json, write_json


def translate_transcription(file_path):
    """
    Translates transcription from Spanish to English.
    """
    subtitles = load_json(file_path)
    
    for subtitle in subtitles:
        original_text = subtitle['text']
        if 'text_en' in subtitle and subtitle['text_en'] != "" : return
        else: 
            translated_text = translate_with_deepl(original_text)
            subtitle['text_en'] = translated_text
    
    # Update the original JSON file with translations
    write_json(subtitles, file_path)
    
    print(f"Translated subtitles updated in {file_path}")