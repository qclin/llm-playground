import requests
from dotenv import load_dotenv
import os
from scripts.process_json import write_json, check_json_file

load_dotenv()
base_url = os.getenv('ASSEMBLY_API_URL')
api_key = os.getenv('ASSEMBLY_API_KEY')
transcribe_url = f'{base_url}/transcript'
headers = {'authorization': api_key}

def transcribe_audio(file_path):
    """
    Uploads an audio file and transcribes it using AssemblyAI.
    """
    # Step 1: Upload audio file to AssemblyAI
    def upload_audio(file_path):
        upload_url = f'{base_url}/upload'
        with open(file_path, 'rb') as f:
            response = requests.post(upload_url, headers=headers, files={'file': f})
        return response.json()['upload_url']
    
    # Step 2: Request transcription
    def request_transcription(audio_url):
        data = {
            "audio_url": audio_url, 
            "language_code": 'es', 
            "speaker_labels":True,
            "speakers_expected": 3, 
            "entity_detection": True
            ### Not available in spanish 
            # "summarization":True, 
            # "summary_type":'paragraph', 
            # "summary_model":'conversational', 
            # "auto_highlights":True
        }

        response = requests.post(transcribe_url, headers=headers, json=data)
        return response.json()['id']
    
    # Step 3: Check transcription status
    def check_transcription(transcription_id):
        polling_url = f"{transcribe_url}/{transcription_id}"
        while True:
            response = requests.get(polling_url, headers=headers)
            status = response.json()['status']
            if status == 'completed':
                return response.json()
            elif status == 'failed':
                raise Exception("Transcription failed!")
    
    audio_url = upload_audio(file_path)
    transcription_id = request_transcription(audio_url)
    transcription_result = check_transcription(transcription_id)
    
    return transcription_result

def save_json(data, file_name, folder_path='transcriptions'):
    # Extract utterances with specific fields
    selected_data = []
    for index, utterance in enumerate(data.get('utterances', [])):
        utterance_data = {
            'sequence': index + 1, 
            'end': utterance['end'],
            'speaker': utterance['speaker'],
            'start': utterance['start'],
            'text': utterance['text'],
            'words': [
                {'text': word['text'], 'start': word['start'], 'end': word['end']}
                for word in utterance.get('words', [])
            ]
        }
        selected_data.append(utterance_data)

    # Create folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{file_name}_utterances.json")

    write_json(selected_data, file_path)

def main(title, season): 
    audio_file_path = f'./Audio/season_{season}/{title}.mp3'
    transcript_file_path = f'./transcriptions/{title}_utterances.json'

    if check_json_file(transcript_file_path):
        return 
    else: 
        transcription_result = transcribe_audio(audio_file_path)
        save_json(transcription_result, os.path.splitext(os.path.basename(audio_file_path))[0])