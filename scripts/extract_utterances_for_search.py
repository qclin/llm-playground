from process_json import load_json, write_json
import os 


file_path = 'transcriptions/las_hijas_overview_season_1.json'
season_data = load_json(file_path)

all_utterances = []
for episode in season_data:
    title = episode['title']['es']
    season = 1
    directory_path = f'transcriptions/season_{season}'
    utterances_path = os.path.join(directory_path, f"{title}_utterances.json")
    
    episode_data = load_json(utterances_path)
    
    simplify_utterances = []
    for utterance in episode_data['utterances']: 
        episode_number = episode['episode']
        season_number = episode['season']
        sequence_number = utterance['sequence'] 
        simplify = {
            'id': f'sq{sequence_number}_ep{episode_number}_s{season_number}',
            'start': utterance['start'], 
            'text': utterance['text'], 
            'text_en': utterance['text_en'], 
            'sequence': sequence_number, 
            'episode': episode_number, 
            'season': season_number, 
        }
        simplify_utterances.append(simplify)
    
    all_utterances = all_utterances + simplify_utterances
    # # Save combined data to a new JSON file
    # output_file = f'transcriptions/utterances/season_{season_number}_episode_{episode_number}.json'
    # write_json(simplify_utterances, output_file)
    
write_json(all_utterances, f'transcriptions/utterances/season_{season_number}.json') 