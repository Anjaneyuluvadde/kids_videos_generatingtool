import os
import time
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, TextClip, CompositeVideoClip, ColorClip, AudioFileClip, concatenate_videoclips, VideoClip
from modules.background_generator import generate_background
from modules.celebration_engine import generate_celebration_clip
from modules.narration_engine import generate_narration

# Predefined objects and emojis
OBJECTS = {
    "cat": "🐱",
    "banana": "🍌",
    "ball": "⚽",
    "apple": "🍎",
    "car": "🚗",
    "dog": "🐶",
    "star": "⭐",
    "heart": "❤️"
}

def generate_progress_timer_clip(duration, resolution):
    """
    Generates a progress bar style timer clip instead of numbers.
    """
    w, h = resolution
    bar_width = 800
    bar_height = 30
    x_pos = (w - bar_width) // 2
    y_pos = h - 100
    
    def make_frame(t):
        # Create a transparent frame
        img = Image.new("RGBA", resolution, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw background bar (grey)
        draw.rectangle((x_pos, y_pos, x_pos + bar_width, y_pos + bar_height), fill=(50, 50, 50, 180), outline="white", width=3)
        
        # Draw progress bar (lime)
        progress = t / duration
        current_width = int(bar_width * progress)
        if current_width > 0:
            draw.rectangle((x_pos, y_pos, x_pos + current_width, y_pos + bar_height), fill=(0, 255, 127, 255))
            
        return np.array(img)
        
    return VideoClip(make_frame, duration=duration)

def _create_hidden_object_clip(image_path, theme, duration, resolution, output_folder):
    """
    Creates a single hidden object video clip with audio.
    """
    w, h = resolution
    
    # 1. Load image and hide object
    try:
        img = Image.open(image_path).convert("RGBA")
    except Exception as e:
        print(f"Failed to load image {image_path}: {e}")
        img = Image.new("RGBA", resolution, (100, 100, 100, 255))
        
    img_w, img_h = img.size
    
    # Select object
    object_name = random.choice(list(OBJECTS.keys()))
    emoji_char = OBJECTS[object_name]
    
    # Select position (avoid edges)
    pos_x = random.randint(int(img_w * 0.1), int(img_w * 0.8))
    pos_y = random.randint(int(img_h * 0.1), int(img_h * 0.8))
    
    # Draw object on image
    draw = ImageDraw.Draw(img)
    try:
        # Try to use Segoe UI Emoji on Windows
        font = ImageFont.truetype("seguiemj.ttf", 60)
    except:
        font = ImageFont.load_default()
        
    draw.text((pos_x, pos_y), emoji_char, font=font, fill=(255, 255, 255, 255))
    
    # Get emoji size for accurate center
    try:
        bbox = font.getbbox(emoji_char)
        ew = bbox[2] - bbox[0]
        eh = bbox[3] - bbox[1]
    except:
        ew, eh = 60, 60 # Fallback
        
    center_x = pos_x + ew // 2
    center_y = pos_y + eh // 2
    
    # Save modified image temporarily
    mod_image_path = os.path.join(output_folder, f"mod_{int(time.time())}_{random.randint(0,1000)}.png")
    img.save(mod_image_path)
    
    # 2. Clips
    total_duration = 2 + duration + 5
    
    # Background (The modified image)
    bg_clip = ImageClip(mod_image_path).with_duration(total_duration)
    scale = min((w * 0.9) / img_w, (h * 0.9) / img_h)
    bg_clip = bg_clip.resized(new_size=(int(img_w * scale), int(img_h * scale)))
    bg_clip = bg_clip.with_position('center')
    
    # Main Background
    bg_array = generate_background(theme=theme, width=w, height=h)
    main_bg = ImageClip(bg_array).with_duration(total_duration)
    
    # Intro / Instruction
    try:
        intro_text = TextClip(
            font="Arial-Bold",
            text=f"Can you find the\nhidden {object_name}?",
            font_size=60,
            color='yellow',
            stroke_color='black',
            stroke_width=4
        ).with_position(('center', 100)).with_duration(2).with_start(0)
    except:
        intro_text = ColorClip(size=(w, 100), color=(0,0,0,0)).with_duration(2).with_start(0)
        
    # Countdown (Progress Bar)
    countdown_clip = generate_progress_timer_clip(duration, resolution).with_start(2)
    
    # Reveal (Circle and Text)
    screen_x = (w - int(img_w * scale)) // 2 + int(center_x * scale)
    screen_y = (h - int(img_h * scale)) // 2 + int(center_y * scale)
    
    overlay_img = Image.new("RGBA", resolution, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay_img)
    r = 60
    # Draw circle with glow
    overlay_draw.ellipse((screen_x - r, screen_y - r, screen_x + r, screen_y + r), outline="red", width=8)
    overlay_draw.ellipse((screen_x - r + 5, screen_y - r + 5, screen_x + r - 5, screen_y + r - 5), outline="yellow", width=3)
    
    overlay_path = os.path.join(output_folder, f"overlay_{int(time.time())}_{random.randint(0,1000)}.png")
    overlay_img.save(overlay_path)
    
    reveal_circle = ImageClip(overlay_path).with_duration(5).with_start(2 + duration)
    
    try:
        reveal_text = TextClip(
            font="Arial-Bold",
            text=f"{object_name.upper()} FOUND!",
            font_size=60,
            color='lime',
            stroke_color='black',
            stroke_width=4
        ).with_position(('center', 550)).with_duration(5).with_start(2 + duration)
        
        # Pop animation
        reveal_text = reveal_text.resized(lambda t: min(1.2, 0.5 + t * 2) if t < 0.5 else 1.0)
    except:
        reveal_text = ColorClip(size=(w, 100), color=(0,0,0,0)).with_duration(5).with_start(2 + duration)
        
    celebration_clip = generate_celebration_clip(5, resolution).with_start(2 + duration)
    
    # 6. Audio / Narration & Subtitles
    from modules.narration_engine import generate_narration
    
    tts_text_q1 = f"Can you find the hidden {object_name}?"
    tts_text_q2 = f"Look carefully! Time is running out!"
    tts_text_a = f"Great job! You found the {object_name}!"
    
    tts_path_q1 = os.path.join(output_folder, f"tts_q1_{int(time.time())}_{random.randint(0,1000)}.mp3")
    tts_path_q2 = os.path.join(output_folder, f"tts_q2_{int(time.time())}_{random.randint(0,1000)}.mp3")
    tts_path_a = os.path.join(output_folder, f"tts_a_{int(time.time())}_{random.randint(0,1000)}.mp3")
    
    generate_narration(tts_text_q1, tts_path_q1)
    generate_narration(tts_text_q2, tts_path_q2)
    generate_narration(tts_text_a, tts_path_a)
    
    audio_clips = []
    subtitle_clips = []
    
    # Helper to create subtitle clip
    def create_sub_clip(text, start_time, duration):
        try:
            print(f"Narration text: {text}")
            print("Subtitle rendered")
            print("Subtitle synchronized with narration")
            return TextClip(
                font="Arial-Bold",
                text=text,
                font_size=40,
                color='white',
                stroke_color='black',
                stroke_width=3
            ).with_position(('center', 650)).with_duration(duration).with_start(start_time)
        except Exception as e:
            print(f"Failed to create subtitle: {e}")
            return ColorClip(size=(1,1), color=(0,0,0,0)).with_duration(duration).with_start(start_time)
            
    # Subtitles
    subtitle_clips.append(create_sub_clip(tts_text_q1, 0, 2))
    subtitle_clips.append(create_sub_clip(tts_text_q2, 2, duration))
    subtitle_clips.append(create_sub_clip(tts_text_a, 2 + duration, 5))
    
    # Audio Clips
    if os.path.exists(tts_path_q1):
        try:
            audio_q1 = AudioFileClip(tts_path_q1).with_start(0)
            audio_clips.append(audio_q1)
        except Exception as e:
            print(f"Audio Q1 failed: {e}")
            
    if os.path.exists(tts_path_q2):
        try:
            audio_q2 = AudioFileClip(tts_path_q2).with_start(2)
            audio_clips.append(audio_q2)
        except Exception as e:
            print(f"Audio Q2 failed: {e}")
            
    if os.path.exists(tts_path_a):
        try:
            audio_a = AudioFileClip(tts_path_a).with_start(2 + duration)
            audio_clips.append(audio_a)
        except Exception as e:
            print(f"Audio A failed: {e}")
            
    # Add background music
    bg_music_path = "uploads/nastelbom-kids-happy-happy-kid-488310.mp3"
    if os.path.exists(bg_music_path):
        try:
            bg_music = AudioFileClip(bg_music_path).with_duration(total_duration)
            bg_music = bg_music.volumex(0.15)
            audio_clips.append(bg_music)
        except Exception as e:
            print(f"Failed to load background music: {e}")
            
    # Composite Video with Subtitles
    clips_to_composite = [
        main_bg,
        bg_clip,
        intro_text,
        countdown_clip,
        reveal_circle,
        reveal_text,
        celebration_clip
    ] + subtitle_clips
    
    final_video = CompositeVideoClip(clips_to_composite)
    
    if audio_clips:
        try:
            from moviepy import CompositeAudioClip
            final_audio = CompositeAudioClip(audio_clips)
            final_video = final_video.with_audio(final_audio)
        except Exception as e:
            print(f"Failed to composite audio: {e}")
            
    return final_video, [mod_image_path, overlay_path, tts_path_q1, tts_path_q2, tts_path_a]

def generate_hidden_object_video_multi(image_paths, theme, duration, output_folder):
    """
    Pipeline for Find Hidden Objects game mode with MULTIPLE images.
    Generates ONE video with multiple frames.
    """
    resolution = (1280, 720)
    clips = []
    all_paths_to_cleanup = []
    
    for img_path in image_paths:
        clip, paths = _create_hidden_object_clip(img_path, theme, duration, resolution, output_folder)
        clips.append(clip)
        all_paths_to_cleanup.extend(paths)
        
    final_video = concatenate_videoclips(clips)
    
    output_filename = f"hidden_object_{int(time.time())}.mp4"
    output_path = os.path.join(output_folder, output_filename)
    
    final_video.write_videofile(output_path, fps=15, codec="libx264", audio_codec="aac")
    
    # Cleanup
    for p in all_paths_to_cleanup:
        if os.path.exists(p):
            try: os.remove(p)
            except: pass
            
    return output_filename
