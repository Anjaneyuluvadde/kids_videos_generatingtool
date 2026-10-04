from PIL import Image
import numpy as np
import os
import random

THEME_MAPPING = {
    "cartoon": "cartoon_network",
    "jungle": "jungle_safari",
    "rainbow": "magical_rainbow",
    "space": "outer_space",
    "learning": "fun_learning"
}

def generate_background(theme="jungle", width=1280, height=720):
    """
    Generates a background image array based on theme by loading provided assets.
    Returns a numpy array suitable for moviepy ImageClip.
    """
    # Map the dropdown value to the theme key
    theme_key = THEME_MAPPING.get(theme, theme)
    
    theme_dir = os.path.join("assets", "themes", theme_key)
    
    if not os.path.exists(theme_dir):
        raise FileNotFoundError(f"Theme directory not found: {theme_dir}")
        
    # Find all images in the directory
    files = [f for f in os.listdir(theme_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not files:
        raise FileNotFoundError(f"No background images found in {theme_dir}. Please add some images (e.g., background_1.png).")
        
    # Select a random background from the list
    asset_path = os.path.join(theme_dir, random.choice(files))
        
    img = Image.open(asset_path)
    # Resize to requested dimensions if necessary
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    return np.array(img)
