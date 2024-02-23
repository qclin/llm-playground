import json
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def translate_text(text, source_language, target_language):
    """
    Translates text from source language to target language using the GPT model.
    """
    response = client.chat.completions.create(
        model="gpt-4",
          messages=[
              {
                'role': "user",
                'content': f"Translate the following text from {source_language} to {target_language}:\n\n{text}"
                }
        ],
        max_tokens=100,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()

def translate_subtitles(json_file_path):
    """
    Translates subtitles from Spanish to English using the OpenAI API.
    """
    with open(json_file_path, 'r') as file:
        subtitles = json.load(file)
    
    for subtitle in subtitles:
        original_text = subtitle['text']
        translated_text = translate_text(original_text, 'es', 'en')
        subtitle['text_en'] = translated_text
    
    # Update the original JSON file with translations
    with open(json_file_path, 'w') as file:
        json.dump(subtitles, file, indent=4)
    
    print(f"Translated subtitles updated in {json_file_path}")

# Example usage
if __name__ == "__main__":
    json_file_path = 'transcriptions/Son estas lágrimas mi manjar-utterances.json'  # Update this to the path of your JSON file
    translate_subtitles(json_file_path)
