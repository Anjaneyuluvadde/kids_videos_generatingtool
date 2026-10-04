import random
from PIL import Image, ImageDraw
import numpy as np
from moviepy import ImageSequenceClip

def generate_celebration_clip(duration, resolution):
    """
    Generates a confetti celebration effect.
    """
    w, h = resolution
    fps = 10
    total_frames = int(duration * fps)
    frames = []
    
    # Pre-generate some random confetti particles
    particles = []
    for _ in range(100):
        particles.append({
            'x': random.randint(0, w),
            'y': random.randint(-h, 0), # Start above screen
            'speed': random.randint(10, 30),
            'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255),
            'size': random.randint(5, 15)
        })
        
    for _ in range(total_frames):
        img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        for p in particles:
            # Draw particle
            r = p['size']
            draw.ellipse([p['x']-r, p['y']-r, p['x']+r, p['y']+r], fill=p['color'])
            
            # Move particle down
            p['y'] += p['speed']
            # Reset if off screen
            if p['y'] > h:
                p['y'] = random.randint(-50, 0)
                p['x'] = random.randint(0, w)
                
        frames.append(np.array(img))
        
    return ImageSequenceClip(frames, fps=fps).with_duration(duration)
