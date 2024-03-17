from dotenv import load_dotenv
from openai import OpenAI
import os
import deepl

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


deepl_api_key = os.environ.get("DEEPL_API_KEY")
translator = deepl.Translator(deepl_api_key)


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

def translate_with_deepl(text, source_lang='ES', target_lang="EN-US"): 
    result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
    # print(result.text)
    return result.text