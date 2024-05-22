import requests
from dotenv import load_dotenv
import os
from scripts.process_json import write_json
import argparse

load_dotenv()
base_url = os.getenv('ASSEMBLY_API_URL')
api_key = os.getenv('ASSEMBLY_API_KEY')
transcribe_url = f'{base_url}/transcript'
headers = {'authorization': api_key}

def transcribe_audio(file_path, title):
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
            "speaker_labels": True,
            "entity_detection": True
            ### Not available in spanish 
            # "summarization":True, 
            # "summary_type":'paragraph', 
            # "summary_model":'conversational', 
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
    print(f'{title} -[transcription_id] {transcription_id}')
    transcription_result = check_transcription(transcription_id)
    
    return transcription_result

def assign_sequence_to_entities(utterances, entities):
    for entity in entities:
        entity_start = entity['start']
        entity_end = entity['end']
        
        # Initialize sequence number for the entity
        entity['sequence'] = None
        
        # Check each utterance to find a match
        for utterance in utterances:
            utterance_start = utterance['start']
            utterance_end = utterance['end']
            
            # Check if entity falls within the range of the utterance
            if entity_start >= utterance_start and entity_end <= utterance_end:
                entity['sequence'] = utterance['sequence']
                break
    return entities

def save_json(data, file_path):
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

    combine_data = {
        "transcript_id": data.get("id", ""),
        "audio_url": data.get('audio_url', ""), 
        "audio_duration": data.get('audio_duration', 0), 
        "text": data.get('text', ""),
        'utterances': selected_data, 
        'entities': assign_sequence_to_entities(selected_data, data.get('entities', []))
    }
    write_json(combine_data, file_path)

def transcibe_and_save(title, season, utterances_path): 
    audio_file_path = f'./Audio/season_{season}/{title}.mp3'
    transcription_result = transcribe_audio(audio_file_path, title)
    save_json(transcription_result, utterances_path)


## For testing in terminal
def main():
    parser = argparse.ArgumentParser(description='Translate Function')
    parser.add_argument('title', type=str, help='Episode Title')
    parser.add_argument('season', type=int, help='Season number')
    parser.add_argument('file_path', type=str, help='File path')

    args = parser.parse_args()
    audio_file_path = f'./Audio/season_{args.season}/{args.title}.mp3'
    transcription_result = transcribe_audio(audio_file_path, args.title)
    save_json(transcription_result, args.file_path)

if __name__ == '__main__':
    main()
