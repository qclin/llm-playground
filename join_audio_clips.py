from pydub import AudioSegment
import os

def join_audio_files(folder_path, output_file):
    # Create a silent segment of one second for the gap
    gap = AudioSegment.silent(duration=1000) # 1000 milliseconds = 1 second

    # Initialize an empty audio segment
    combined = AudioSegment.empty()

    # List and sort all mp3 files in the folder
    audio_files = sorted([file for file in os.listdir(folder_path) if file.endswith('.mp3')])

    # Loop through each file, adding it and the gap to the combined audio
    for file in audio_files:
        audio = AudioSegment.from_mp3(os.path.join(folder_path, file))
        combined += audio + gap

    # Export the combined audio to a single file
    combined.export(output_file, format='mp3')
    print(f'Combined audio saved as {output_file}')

def main():
    folder_path = './las_hijas_de_felipe/la_leche_polifonica/audio_clips' # Replace with your folder path
    output_file = 'combined_audio.mp3' # Replace with your desired output file name
    join_audio_files(folder_path, output_file)

if __name__ == "__main__":
    main()
