import os
import subprocess
import whisper

def extract_audio(video_path, audio_path):
    """Extracts audio from the video using FFmpeg."""
    print(f"🔄 Extracting audio from: {video_path}")

    video_path = f'"{video_path}"'  # Handle spaces in filenames
    audio_path = f'"{audio_path}"'

    command = f'ffmpeg -i {video_path} -q:a 0 -map a {audio_path} -y'
    subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if not os.path.exists(audio_path.strip('"')):
        raise FileNotFoundError(f"❌ Audio extraction failed! File not found: {audio_path}")

    print(f"✅ Audio extracted: {audio_path}")

def transcribe_audio(audio_path, srt_output_path, formatted_text_output):
    """Transcribes the extracted audio and saves:
       - SRT subtitles
       - Fully formatted paragraph transcript
    """
    print(f"🔄 Transcribing audio: {audio_path}")

    if not os.path.exists(audio_path.strip('"')):
        raise FileNotFoundError(f"❌ Audio file not found for transcription: {audio_path}")

    model = whisper.load_model("small")  # Use "medium" or "large" for better accuracy
    result = model.transcribe(audio_path.strip('"'), fp16=False)

    full_text = []  # Store text for formatted paragraphs

    with open(srt_output_path, "w") as srt_file:
        for i, segment in enumerate(result["segments"]):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]

            # Write to SRT file
            srt_file.write(f"{i+1}\n{format_time(start)} --> {format_time(end)}\n{text}\n\n")

            # Collect text for paragraph formatting
            full_text.append(text)

    # Convert to a properly formatted paragraph
    formatted_paragraphs = " ".join(full_text).replace("..", ".")  # Ensure no double dots

    with open(formatted_text_output, "w") as formatted_file:
        formatted_file.write(formatted_paragraphs)

    print(f"✅ Subtitles saved as: {srt_output_path}")
    print(f"✅ Fully formatted paragraph file saved as: {formatted_text_output}")

def format_time(seconds):
    """Convert time in seconds to SRT timestamp format (HH:MM:SS,ms)."""
    millisec = int((seconds % 1) * 1000)
    sec = int(seconds) % 60
    minutes = (int(seconds) // 60) % 60
    hours = (int(seconds) // 3600)
    return f"{hours:02}:{minutes:02}:{sec:02},{millisec:03}"

def video_to_subtitles(video_path):
    """Complete function to convert video to:
       - Subtitles (SRT)
       - Fully formatted paragraph transcript
    """
    base_path = os.path.splitext(video_path)[0]
    audio_path = f"{base_path}.wav"
    srt_output_path = f"{base_path}.srt"
    formatted_text_output = f"{base_path}_formatted.txt"

    try:
        extract_audio(video_path, audio_path)
        transcribe_audio(audio_path, srt_output_path, formatted_text_output)

        print(f"🎉 Process Complete!")
        print(f"📜 Subtitles: {srt_output_path}")
        print(f"📜 Fully Formatted Paragraph: {formatted_text_output}")

    except Exception as e:
        print(f"❌ Error: {e}")

# Example Usage:
video_file = ("video file link")
video_to_subtitles("/home/aisha/video_to_string_amazon/test.mp4")