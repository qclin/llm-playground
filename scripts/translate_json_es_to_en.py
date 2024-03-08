from .translate_text import translate_text 
from .process_json import load_json, write_json


def translate_transcription(file_path):
    """
    Translates subtitles from Spanish to English using the OpenAI API.
    """
    
    subtitles = load_json(file_path)
    
    for subtitle in subtitles:
        original_text = subtitle['text']
        translated_text = translate_text(original_text, 'es', 'en')
        subtitle['text_en'] = translated_text
    
    # Update the original JSON file with translations
    write_json(subtitles, file_path)
    
    print(f"Translated subtitles updated in {file_path}")

# # Example usage
# if __name__ == "__main__":
#     json_file_path = 'transcriptions/Disecciones conventuales, anatomía barroca-utterances.json'  # Update this to the path of your JSON file
#     translate_subtitles(json_file_path)
