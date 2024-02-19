from pydub import AudioSegment
import math
import os

class SplitAudio():
    def __init__(self, filepath, audio_folder_path,  file_name):
        self.folder = audio_folder_path
        self.filename = file_name        
        self.audio = AudioSegment.from_mp3(filepath)
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(self.folder + '\\' + split_filename, format="mp3")
        
    def multiple_split(self, min_per_split):
        total_mins = math.ceil(self.get_duration() / 60)
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i, i+min_per_split, split_fn)
            print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splited successfully')

audio_folder_path = os.path.join('Audio')
file_name = 'La leche polifónica.mp3'
file_path = os.path.join(audio_folder_path, file_name)

split_wav = SplitAudio(file_path, audio_folder_path, file_name)
split_wav.multiple_split(min_per_split=20)