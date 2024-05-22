from process_json import load_json, write_json
import os 


file_path = 'show-note.json'
show_note_data = load_json(file_path)

episodes = show_note_data["episodes"]["items"]
simplify_episodes = []
for episode in episodes:
    simplify = {
        'id':episode['id'],
        'description': episode["description"], 
        "duration_ms": episode["duration_ms"], 
        'title': episode["name"], 
        "release_date": episode["release_date"]
    }
    simplify_episodes.append(simplify)
write_json(simplify_episodes, f'show_note_simplify.json') 