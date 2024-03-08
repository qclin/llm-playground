# NOT USED 

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
)

audio_file = open("Audio/2_La leche polifónica.mp3", "rb")

completion = client.audio.translations.create(
  model="whisper-1",
  file=audio_file
)

print(completion.text)
