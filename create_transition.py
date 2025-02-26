from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os

# Input paths
image_folder = "Images/"  # Folder containing images
audio_file = "Audio/arti audio.mp3"  # Path to your audio file
output_video = "output_video.mp4"  # Output video file

# Get list of images sorted by name
images = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith((".png", ".jpg", ".jpeg"))])

# Parameters
fps = 24  # Frames per second
duration_per_image = 3  # Duration for each image
transition_duration = 0.5  # Smooth fade transition duration
resolution = (1920, 1080)  # Full HD 16:9 resolution

# Create individual clips with proper resizing, cropping, and zoom-in effect
clips = []
for img in images:
    clip = ImageClip(img)

    # Get aspect ratio of the image
    img_ratio = clip.w / clip.h
    target_ratio = 16 / 9  # 1920/1080

    if img_ratio > target_ratio:
        # Image is wider than 16:9 -> Resize by height, then crop width
        clip = clip.resize(height=resolution[1])
        clip = clip.crop(x_center=clip.w / 2, width=resolution[0], height=resolution[1])
    else:
        # Image is taller than 16:9 -> Resize by width, then crop height
        clip = clip.resize(width=resolution[0])
        clip = clip.crop(y_center=clip.h / 2, width=resolution[0], height=resolution[1])

    # Apply zoom-in effect (Ken Burns effect)
    zoom_clip = clip.set_duration(duration_per_image).resize(lambda t: 1 + 0.03 * t)  # 3% zoom-in

    # Apply smooth transition
    zoom_clip = zoom_clip.crossfadein(transition_duration)

    clips.append(zoom_clip)

# Concatenate clips with smooth transitions
final_clip = concatenate_videoclips(clips, method="compose")

# Load and adjust audio
audio = AudioFileClip(audio_file)

# Match audio and video duration
if final_clip.duration > audio.duration:
    final_clip = final_clip.subclip(0, audio.duration)
else:
    audio = audio.subclip(0, final_clip.duration)

# Add audio to the video
final_clip = final_clip.set_audio(audio)

# Save the final video with smooth transitions
final_clip.write_videofile(output_video, codec="libx264", fps=fps, audio_codec="aac")

print(f"Video saved as {output_video}")
