from moviepy.editor import VideoFileClip, concatenate_videoclips

# Load the typewriter effect video
typewriter_clip = VideoFileClip("typewriter_with_sound.mp4")

# Load the main video
main_clip = VideoFileClip("output_video.mp4")

# Ensure both videos have the same resolution
target_resolution = (max(typewriter_clip.size[0], main_clip.size[0]), 
                     max(typewriter_clip.size[1], main_clip.size[1]))

typewriter_clip = typewriter_clip.resize(target_resolution)
main_clip = main_clip.resize(target_resolution)

# Concatenate both videos
final_video = concatenate_videoclips([typewriter_clip, main_clip])

# Export the final merged video
final_video.write_videofile("final_combined_video.mp4", codec="libx264", fps=10, audio_codec="aac")

print("Final video saved as final_combined_video.mp4")