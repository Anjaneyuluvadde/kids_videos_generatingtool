from moviepy import ColorClip

def generate_timer_clip(duration, resolution):
    """
    Generates a countdown timer progress bar clip (slides out).
    Does not require ImageMagick.
    """
    w, h = resolution
    bar_h = 30
    # Bright coral red bar
    bar = ColorClip(size=(w, bar_h), color=(255, 99, 71)).with_duration(duration)
    
    # Animate sliding to the left
    # At t=0, x=0. At t=duration, x=-w
    bar = bar.with_position(lambda t: (int(-w * (t / duration)), h - bar_h))
    
    return bar

def add_timer_sound(audio_clip):
    """
    Mock for adding ticking sound.
    """
    return audio_clip
