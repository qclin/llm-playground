from process_json import load_json, write_json
import os 

def count_words(string):
    words = string.split()
    return len(words)

def duration_to_minutes(duration):
    """Converts a duration string in the format 'HH:MM:SS' to minutes."""
    minutes, seconds = map(int, duration.split(':'))
    total_minutes = minutes + seconds / 60.0
    return total_minutes

def calculate_wpm(transcription, duration):
    """Calculates words per minute (WPM) given a transcription and audio duration."""
    num_words = count_words(transcription)
    duration_minutes = duration_to_minutes(duration)
    wpm = num_words / duration_minutes
    return wpm, num_words


file_path = 'transcriptions/las_hijas_overview_season_1.json'
season_data = load_json(file_path)

for episode in season_data:
    title = episode['title']['es']
    season = 1
    directory_path = f'transcriptions/season_{season}'
    utterances_path = os.path.join(directory_path, f"{title}_utterances.json")
    
    episode_data = load_json(utterances_path)
    
    wpm, num_words = calculate_wpm(episode_data["text"], episode["duration"])
    
    print(f'{title} ----- duration: {episode["duration"]} word_count: {num_words} wpm: {wpm:.2f}' )
    wpm_formatted = round(wpm, 2)

    episode["words_per_minute"] = wpm_formatted
    episode["word_count"] = num_words

write_json(season_data, file_path)