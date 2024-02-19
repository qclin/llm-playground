import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def translate_text(text, source_lang='es', target_lang='en'):
    try:
        response = client.chat.completions.create(
          model="gpt-4",
          messages=[
              {
                'role': "user",
                'content': f"Translate the following text from {source_lang} to {target_lang}:\n\n{text}"
                }
            ],
          temperature=0.3,
          max_tokens=60,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )

        print(response.choices[0].message.content.strip())
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

def translate_srt(file_path, output_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()

        translated_content = ""
        for line in content:
            if line.strip().isdigit() or '-->' in line:
                translated_content += line
            elif line.strip():
                translated_line = translate_text(line.strip(), 'es', 'en')
                translated_content += translated_line + '\n'
            else:
                translated_content += '\n'

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(translated_content)

        print(f"Translation complete. Output file: {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
translate_srt('./tears_es.srt', 'tears_en.srt')