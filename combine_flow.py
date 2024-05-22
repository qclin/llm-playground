from scripts.process_json import load_json, check_json_file
from transcribe_assembly_json import transcibe_and_save as transcribe
from highlights import main as find_highlights
from scripts.translate_json_es_to_en import translate_transcription
from scripts.map_sequence_to_time import map_sequence_to_time
import os 

file_path = 'transcriptions/las_hijas_overview_season_2.json'
season_data = load_json(file_path)

for episode in season_data:
    title = episode['title']['es']
    season = 2
    directory_path = f'transcriptions/season_{season}'

    # Create folder if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)
    utterances_path = os.path.join(directory_path, f"{title}_utterances.json")
    topics_path = os.path.join(directory_path, f"{title}_topics.json")

    print(utterances_path, check_json_file(utterances_path))
    print(topics_path, check_json_file(topics_path))
    
    if check_json_file(utterances_path) is False: 
        transcribe(title, season, utterances_path)

    translate_transcription(utterances_path)

    # Find highlights, entities and citation if we haven't process it yet
    if check_json_file(topics_path) is False:
        find_highlights(utterances_path, topics_path)
    
    map_sequence_to_time(utterances_path, topics_path)