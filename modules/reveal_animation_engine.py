from moviepy import ImageClip, vfx

def generate_reveal_clip(image_path, duration, resolution):
    """
    Generates a reveal animation for the original image.
    """
    try:
        img_clip = ImageClip(image_path).with_duration(duration)
        
        # Center and resize to fit
        w, h = resolution
        img_w, img_h = img_clip.size
        scale = min((w * 0.9) / img_w, (h * 0.6) / img_h)
        img_clip = img_clip.resized(new_size=(int(img_w * scale), int(img_h * scale)))
        img_clip = img_clip.with_position('center')
        
        # Apply fade in effect
        img_clip = img_clip.with_effects([vfx.FadeIn(1.0)])
        
        return img_clip
    except Exception as e:
        print(f"Reveal animation failed: {e}")
        # Return a black clip or similar if failed, but try to return something
        from moviepy import ColorClip
        return ColorClip(size=resolution, color=(0,0,0)).with_duration(duration)
