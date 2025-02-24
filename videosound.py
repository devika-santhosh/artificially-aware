from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips

# Load video
video = VideoFileClip("typewriter_effect.mp4")

# Load typewriter sound
audio = AudioFileClip("keystroke.mp3")  # Use "keystroke.mp3" if it's an MP3 file

# Calculate how many times the sound should repeat to match video length
repeat_count = int(video.duration / audio.duration) + 1

# Create a looped audio track
looped_audio = concatenate_audioclips([audio] * repeat_count)

# Trim audio to match video duration
final_audio = looped_audio.set_duration(video.duration)

# Set audio to video
final_video = video.set_audio(final_audio)

# Save the output
final_video.write_videofile("typewriter_with_sound.mp4", codec="libx264", fps=10, audio_codec="aac")

print("Merged video saved as typewriter_with_sound.mp4")

