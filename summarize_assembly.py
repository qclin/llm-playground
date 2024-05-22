import requests
from dotenv import load_dotenv
import os
from scripts.process_json import load_json, write_json


load_dotenv()
base_url = 'https://api.assemblyai.com'
api_key = os.getenv('ASSEMBLY_API_KEY')
headers = {'authorization': api_key}


def try_post_request(url, data): 
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx, 5xx)
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"Error 404: The requested resource was not found at {url}")
        else:
            print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    else:
        # Process the response if everything is fine
        print(f"Success! {response.json()}")
        return response.json()

def summarize_audio(transcript_id):
    summarize_url = f'{base_url}/lemur/v3/generate/summary'
    data = {
        "transcript_ids": [transcript_id],
        "context": "This is podcast transcript.",
        "final_model": "default",
        "temperature": 0,
    }
    return try_post_request(summarize_url, data)

def categorize_audio(transcript_id): 
    task_url = f'{base_url}/lemur/v3/generate/task'
    data = {
        "transcript_ids": [transcript_id],
        "prompt": "List topics discussed in the podcast and return a list of object with the field topic and start timestamp in miliseconds. Plese format the response as a valid json list",
        "context": "This is podcast transcript.",
        "final_model": "default",
        "temperature": 0,
    }
    return try_post_request(task_url, data)

def load_season_data(season): 
    file_path = f'transcriptions/las_hijas_overview_season_{season}.json'
    season_data = load_json(file_path)
    for episode in season_data:
        transcript_id = episode['transcript_id']
        # data = summarize_audio(transcript_id)
        # episode["summary"]["assembly_lemur"] = data["response"]
        data = categorize_audio(transcript_id)
        write_json(data["response"], f'transcriptions/topics/season_{season}/{episode["title"]["es"]}.json')
    
if __name__ == '__main__':
    load_season_data(1)
