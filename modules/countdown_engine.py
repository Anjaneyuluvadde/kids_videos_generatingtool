from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from moviepy import ImageClip, concatenate_videoclips

def create_number_image(number, resolution, font_path=None):
    """
    Draws a number on a transparent canvas.
    """
    w, h = resolution
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Try to load a large font
    try:
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, 300)
        else:
            font = ImageFont.truetype("arial.ttf", 300)
    except:
        font = ImageFont.load_default()
        
    text = str(number)
    
    # Center text
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
    except:
        # Fallback for older Pillow
        tw, th = draw.textsize(text, font=font)
        
    draw.text(((w - tw) // 2, (h - th) // 2), text, font=font, fill=(255, 215, 0, 255)) # Gold color
    
    return np.array(img)

def generate_countdown_clip(duration, resolution):
    """
    Generates a countdown video clip from duration down to 1.
    """
    clips = []
    # Duration per number is 1 second
    num_duration = 1.0
    
    for i in range(duration, 0, -1):
        img_array = create_number_image(i, resolution)
        clip = ImageClip(img_array).with_duration(num_duration)
        clips.append(clip)
        
    return concatenate_videoclips(clips)
