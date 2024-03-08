# NOT USED 

import assemblyai as aai
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv('ASSEMBLY_API_KEY')
aai.settings.api_key = api_key
FILE_URL = "./Audio/Son estas lágrimas mi manjar.mp3"

config = aai.TranscriptionConfig(
  speaker_labels=True, 
  language_code='es',
  summarization=True, 
  summary_type='paragraph', 
  summary_model='conversational', 
  auto_highlights=True
)

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(
  FILE_URL,
  config=config
)

for utterance in transcript.utterances:
  print(f"{utterance.speaker}: {utterance.text}")


for result in transcript.auto_highlights.results:
    print(f"Highlight: {result.text}, Count: {result.count}, Rank: {result.rank}, Timestamps: {result.timestamps}")

print(transcript.summary)