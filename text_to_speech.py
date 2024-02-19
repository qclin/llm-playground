from pathlib import Path
from openai import OpenAI
import os
import json 

client = OpenAI()

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Generate audio from text
def text_to_speech(text, speaker, index, output_folder):
    
    response = client.audio.speech.create(
        model="tts-1",
        voice="shimmer" if speaker == 'Carmen' else 'nova',
        input=text
    )

    filename = f"{output_folder}/{index:03d}_{speaker}.mp3"
    response.stream_to_file(filename)
    print(f"Saved {filename}")


def main():
    json_file_path = './process/la_leche_polifonica/conversation.json'
    output_folder = './process/la_leche_polifonica/audio_clips'
    conversations = load_json(json_file_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for index, item in enumerate(conversations):
        text_to_speech(item['content'], item['speaker'], index, output_folder)

if __name__ == "__main__":
    main()


# def process_text_files(input_folder, output_folder):
#     # tts = TextToSpeechConverter()  # Replace with actual TTS initialization

#     # Create the output folder if it doesn't exist
#     os.makedirs(output_folder, exist_ok=True)

#     # Process each file in the input folder
#     for file_name in os.listdir(input_folder):
#         if file_name.endswith('.txt'):
#             file_path = os.path.join(input_folder, file_name)
#             text = read_text_file(file_path)

#             # Convert text to speech
#             response = client.audio.speech.create(
#                 model="tts-1",
#                 voice="alloy",
#                 input=text
#             )
#             # Save the audio file
#             output_file_path = os.path.join(output_folder, file_name.replace('.txt', '.mp3'))
#             response.stream_to_file(output_file_path)

# # Example usage
# input_folder = 'AudioText/chunk'  # Replace with the path to your text files
# output_folder = 'clips'  # The folder where audio files will be saved
# process_text_files(input_folder, output_folder)