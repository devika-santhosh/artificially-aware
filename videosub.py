import cv2
import numpy as np
import imageio
import textwrap
import time

# Define parameters
text = "Rise, Shine, Conquer."  
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
thickness = 2
color = (255, 255, 255)  # White text
bg_color = (0, 0, 0)  # Black background
fps = 10  # Frame rate

# Video size
width, height = 800, 400  # Video frame size
line_spacing = 40  # Space between lines

# Define text wrapping width (approx max characters per line)
char_per_line = 25
wrapped_text = textwrap.wrap(text, width=char_per_line)

# Calculate total text height for center alignment
text_height = len(wrapped_text) * line_spacing
start_y = (height - text_height) // 2  # Center Y position

# List to store frames
frames = []
img = np.zeros((height, width, 3), dtype=np.uint8)  # Background frame

typed_text = [""] * len(wrapped_text)  # Empty list to store typed text per line

# Typewriter effect
for i in range(len(wrapped_text)):  # Iterate through each line
    for char in wrapped_text[i]:  # Iterate through each character
        typed_text[i] += char  # Add one letter at a time
        frame = img.copy()

        # Draw each completed line so far
        for j in range(i + 1):  
            text_size = cv2.getTextSize(typed_text[j], font, font_scale, thickness)[0]
            text_x = (width - text_size[0]) // 2  # Center text horizontally
            text_y = start_y + j * line_spacing  # Adjust vertical position
            
            cv2.putText(frame, typed_text[j], (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)

        frames.append(frame)
        time.sleep(0.1)  # Typing delay

# Save video
imageio.mimsave("typewriter_effect.mp4", frames, fps=fps)
print("Video saved as typewriter_effect.mp4")

