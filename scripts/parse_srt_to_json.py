import re
import json

def parse_srt(srt_path):
    # Regular expression to match the SRT components: sequence number, timestamps, and text
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL)
    
    with open(srt_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    matches = pattern.findall(content)
    
    # Convert matches into a list of dictionaries
    subtitles = [
        {"sequence": int(match[0]),
         "start": match[1],
         "end": match[2],
         "text": match[3].replace('\n', ' ')}  # Replace newline characters in the text with a space
        for match in matches
    ]
    
    return subtitles

def write_json(data, json_path):
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Example usage
srt_path = 'tears_en.srt'  # Path to your SRT file
json_path = 'tears_en.json'  # Output JSON file path

subtitles = parse_srt(srt_path)
write_json(subtitles, json_path)

print(f"JSON file has been created: {json_path}")
