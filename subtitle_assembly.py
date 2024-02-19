import requests
import time
from dotenv import load_dotenv
import os


load_dotenv()
base_url = os.getenv('ASSEMBLY_API_URL')
api_key = os.getenv('ASSEMBLY_API_KEY')
transcribe_url = f'{base_url}/transcript'
headers = {'authorization': api_key}

with open("./Audio/Son estas lágrimas mi manjar.mp3" , "rb") as f:
  response = requests.post(base_url + "/upload",
                          headers=headers,
                          data=f)

upload_url = response.json()["upload_url"]

data = {
    "audio_url": upload_url, 
    "language_code": 'es', 
    "speaker_labels":True,
    "speakers_expected": 3
}

url = base_url + "/transcript"
response = requests.post(url, json=data, headers=headers)

transcript_id = response.json()['id']

polling_endpoint = f"{base_url}/transcript/{transcript_id}"

while True:
  transcription_result = requests.get(polling_endpoint, headers=headers).json()

  if transcription_result['status'] == 'completed':
    break

  elif transcription_result['status'] == 'error':
    raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

  else:
    time.sleep(3)

def get_subtitle_file(transcript_id, file_format):
    if file_format not in ["srt", "vtt"]:
        raise ValueError("Invalid file format. Valid formats are 'srt' and 'vtt'.")

    url = f"{base_url}/transcript/{transcript_id}/{file_format}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        raise RuntimeError(f"Failed to retrieve {file_format.upper()} file: {response.status_code} {response.reason}")

# subtitle_text = get_subtitle_file(transcript_id, "vtt")
subtitle_text = get_subtitle_file(transcript_id, "srt")
# File path for the SRT file
srt_file_path = f'transcripts/es/tears-{transcript_id}.srt'

# Write the SRT content to a file
with open(srt_file_path, 'w') as file:
    file.write(subtitle_text)

print(f"SRT content has been written to {srt_file_path}")

