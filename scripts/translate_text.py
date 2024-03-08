import os
from openai import OpenAI
# from googletrans import Translator

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def translate_text(text, source_language='es', target_language='en'):
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
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()

# def translate_text_google(text, source_language='es', target_language='en'):

#     translator = Translator()
#     translated_text = translator.translate(text, src=source_language, dest=target_language)

#     return translated_text.text