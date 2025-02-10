import os
import subprocess

video_path = '/home/aisha/video_to_string_amazon.mp4'
base_path = os.path.splitext(video_path)[0]
audio_path = f"{base_path}.wav"
srt_output_path = f"{base_path}.srt"
formatted_text_output = f"{base_path}_formatted.txt"


video_path = f'"{video_path}"'  # Handle spaces in filenames
audio_path = f'"{audio_path}"'

command = f'ffmpeg -i {video_path} -q:a 0 -map a {audio_path} -y'
subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if not os.path.exists(audio_path.strip('"')):
        raise FileNotFoundError(f"Audio extraction failed! File not found: {audio_path}")

print(f"Audio extracted: {audio_path}")