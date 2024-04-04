from moviepy.editor import VideoFileClip

# Assuming 'input_video_filename' is a variable holding the name of the input video file
input_video_filename = input(
    "Enter the name of the input video file (e.g., 'input_video.mp4'): ")

# Generate the output video filename by adding a prefix "s" to the input filename
output_video_filename = "s" + input_video_filename
output_audio_filename = "a" + input_video_filename + ".mp3"

# Load the video file
video_clip = VideoFileClip(input_video_filename)

# Set the audio of the clip to None to remove it
video_clip_no_audio = video_clip.without_audio()

# Write the modified video to a file
video_clip_no_audio.write_videofile(output_video_filename)
print(f"Video without audio saved as {output_video_filename}")

# Extract the audio from the original video
audio = video_clip.audio

# Write the audio to a file
audio.write_audiofile(output_audio_filename)
print(f"Audio extracted and saved as {output_audio_filename}")
