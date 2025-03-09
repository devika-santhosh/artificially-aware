from moviepy.editor import AudioFileClip, VideoClip
import os, math
from PIL import Image
import numpy as np

def generate_video(image_folder, audio_file, output_video, t=None):
    """
    Generate a video with optional duration `t`. If `t` is not provided, use the audio length.
    """
    # Get list of images sorted by name (case-insensitive)
    images = sorted([
        os.path.join(image_folder, img)
        for img in os.listdir(image_folder)
        if img.lower().endswith((".png", ".jpg", ".jpeg"))
    ])

    # Parameters
    fps = 24
    duration_per_image = 3      # Duration for each image in seconds
    transition_duration = 1.0   # Duration of crossfade in seconds
    resolution = (1920, 1080)   # Full HD 16:9 resolution

    # Load audio and get final video duration
    audio = AudioFileClip(audio_file)
    final_video_duration = t if t is not None else audio.duration  # Use `t` if provided, else use audio duration

    # Compute effective duration per clip (overlap accounts for crossfade)
    effective_duration = duration_per_image - transition_duration
    # Total number of clips needed
    total_images_needed = math.ceil((final_video_duration - duration_per_image) / effective_duration) + 1

    # Repeat images as needed to fill all clips
    repeated_images = (images * ((total_images_needed // len(images)) + 1))[:total_images_needed]

    # --- Preprocess Images ---
    def load_and_process_image(path, resolution):
        """Load an image, resize and crop it to maintain a 16:9 aspect ratio."""
        img = Image.open(path).convert("RGB")
        w, h = img.size
        target_ratio = 16 / 9
        img_ratio = w / h
        if img_ratio > target_ratio:
            # Image is wider: resize by height, crop width.
            new_h = resolution[1]
            new_w = int(w * new_h / h)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            left = (new_w - resolution[0]) // 2
            img = img.crop((left, 0, left + resolution[0], resolution[1]))
        else:
            # Image is taller: resize by width, crop height.
            new_w = resolution[0]
            new_h = int(h * new_w / w)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            top = (new_h - resolution[1]) // 2
            img = img.crop((0, top, resolution[0], top + resolution[1]))
        return np.array(img)

    # Preload each unique image (avoid repeated processing)
    processed_images = {}
    for img_path in set(repeated_images):
        processed_images[img_path] = load_and_process_image(img_path, resolution)

    # --- Zoom Effect Helper ---
    def apply_zoom(frame, t, zoom_rate=0.03):
        """
        Apply a zoom-in effect to the frame.
        Zoom factor = 1 + zoom_rate * t.
        """
        zoom_factor = 1 + zoom_rate * t
        H, W, _ = frame.shape
        new_W = int(W / zoom_factor)
        new_H = int(H / zoom_factor)
        left = (W - new_W) // 2
        top = (H - new_H) // 2
        cropped = frame[top:top+new_H, left:left+new_W, :]
        pil_cropped = Image.fromarray(cropped)
        pil_resized = pil_cropped.resize((W, H), Image.LANCZOS)
        return np.array(pil_resized)

    # --- Frame Generator Function ---
    def make_frame(t):
        """
        For a given time t, determine which image clip(s) to use,
        apply the zoom effect, and blend frames during crossfade.
        """
        # Determine the current clip index based on effective duration
        i = int(t // effective_duration)
        if i >= total_images_needed:
            i = total_images_needed - 1
        local_t = t - i * effective_duration

        # If not in crossfade region (or for the very first clip), use a single image.
        if i == 0 or local_t >= transition_duration:
            base_img = processed_images[repeated_images[i]]
            return apply_zoom(base_img, local_t)
        else:
            # During crossfade: blend the tail of the previous clip with the current clip.
            alpha = local_t / transition_duration
            # For the previous clip, determine the corresponding time (its tail)
            t_prev = duration_per_image - transition_duration + local_t
            base_img_prev = processed_images[repeated_images[i-1]]
            base_img_curr = processed_images[repeated_images[i]]
            frame_prev = apply_zoom(base_img_prev, t_prev)
            frame_curr = apply_zoom(base_img_curr, local_t)
            # Linear blend between previous and current frames
            blend = ((1 - alpha) * frame_prev.astype(np.float32) +
                     alpha * frame_curr.astype(np.float32))
            return blend.astype(np.uint8)

    # Create a VideoClip that generates frames on the fly
    video_clip = VideoClip(make_frame, duration=final_video_duration)
    video_clip = video_clip.set_audio(audio.subclip(0, final_video_duration))  # Subclip audio to match duration

    # Write out the video
    video_clip.write_videofile(
        output_video,
        fps=fps,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        threads=4
    )

    video_clip.close()
    audio.close()

# Example usage
image_folder = "Images/"
audio_file = "Audio/arti audio.mp3"
output_video = "output_video.mp4"

# Generate video with custom duration (e.g., 120 seconds)
generate_video(image_folder, audio_file, output_video, t=30)

# Generate video with original audio length
# generate_video(image_folder, audio_file, output_video)