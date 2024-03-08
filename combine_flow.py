from scripts.process_json import load_json
from transcribe_assembly_json import main as transcribe
from highlights import main as find_highlights
from scripts.translate_json_es_to_en import translate_transcription
file_path = 'transcriptions/las_hijas_overview_season_1.json'
season_data = load_json(file_path)

for episode in season_data:
    title = episode['title']['es']
    transcribe(title, 1)
    translate_transcription(f'transcriptions/{title}_utterances.json')
    find_highlights(title)