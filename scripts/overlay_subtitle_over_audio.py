from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

# Specify your MP3 and SRT file paths
audio_file_path = './Audio/Son estas lágrimas mi manjar.mp3'
srt_file_path = './tears_en.srt'

# Load your MP3 file
audio_clip = AudioFileClip(audio_file_path)

# Generate a blank color clip as video background
video_clip = ColorClip(size=(1920, 1080), color=(0,0,0), duration=audio_clip.duration)

# Set the audio of the color clip to be your mp3 file
video_clip = video_clip.set_audio(audio_clip)

# Function to apply styling to subtitles
def make_textclip(txt):
    # Here you can specify the font, fontsize, color, etc.
    return TextClip(txt, font='NewCenturySchlbk-Roman', fontsize=48, color='DeepPink')

# Load the subtitles from the SRT file and apply styling
subtitles = SubtitlesClip(srt_file_path, make_textclip)

# Overlay the subtitles on your video clip
final_clip = CompositeVideoClip([video_clip, subtitles.set_position(('center','center'))])

# Specify the output video file path
output_video_path = 'output_tears2.mp4'

# Write the result to a file (many options available!)
final_clip.write_videofile(output_video_path, codec='libx264', fps=24)

print(f"Video created successfully: {output_video_path}")
# print(f"Colors - {', '.join(str(c) for c in TextClip.list('color')) }")