from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
import os

# Input paths
image_folder = "Images/"  # Folder containing images
audio_file = "Audio/arti audio.mp3"  # Path to your audio file
output_video = "output_video.mp4"  # Output video file

# Get list of images sorted by name
images = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith((".png", ".jpg", ".jpeg"))])

# Create a video clip from images
clip = ImageSequenceClip(images, fps=1)  # Adjust fps (frames per second) as needed

# Load audio
audio = AudioFileClip(audio_file)

# Set audio duration to match video duration
if clip.duration > audio.duration:
    clip = clip.subclip(0, audio.duration)  # Trim video to match audio length
else:
    audio = audio.subclip(0, clip.duration)  # Trim audio to match video length

# Add audio to the video
final_clip = clip.set_audio(audio)

# Save the final video
final_clip.write_videofile(output_video, codec="libx264", fps=24)  # Adjust fps if needed

print(f"Video saved as {output_video}")
