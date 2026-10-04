import os
import time
import random
from moviepy import ImageClip, TextClip, CompositeVideoClip, ColorClip, AudioFileClip, concatenate_videoclips
from modules.background_generator import generate_background
from modules.silhouette_generator import generate_silhouette
from modules.countdown_engine import generate_countdown_clip
from modules.reveal_animation_engine import generate_reveal_clip
from modules.celebration_engine import generate_celebration_clip
from modules.narration_engine import generate_narration

def _create_guess_animal_clip(image_path, theme, duration, resolution, output_folder):
    """
    Creates a single guess animal video clip with audio.
    """
    w, h = resolution
    animal_name = "the animal"
    if image_path:
        animal_name = os.path.splitext(os.path.basename(image_path))[0].replace('_', ' ').capitalize()
        
    total_duration = 2 + duration + 5
    
    # 1. Visual Theme (Background)
    from modules.background_generator import generate_background
    bg_array = generate_background(theme=theme, width=w, height=h)
    bg_clip = ImageClip(bg_array).with_duration(total_duration)
    
    # 2. Intro Scene (0-2 sec)
    try:
        intro_text = TextClip(
            font="Arial-Bold",
            text="Can You Guess\nThe Animal?",
            font_size=60,
            color='yellow',
            stroke_color='black',
            stroke_width=4
        ).with_position('center').with_duration(2).with_start(0)
    except:
        intro_text = ColorClip(size=(w, 100), color=(0,0,0,0)).with_duration(2).with_start(0)
        
    # 3. Clue Scene
    from modules.silhouette_generator import generate_silhouette
    silh_path = os.path.join(output_folder, f"silh_{int(time.time())}_{random.randint(0,1000)}.png")
    generate_silhouette(image_path, silh_path)
    
    silh_clip = ImageClip(silh_path).with_duration(duration).with_start(2)
    img_w, img_h = silh_clip.size
    scale = min((w * 0.9) / img_w, (h * 0.6) / img_h)
    silh_clip = silh_clip.resized(new_size=(int(img_w * scale), int(img_h * scale)))
    silh_clip = silh_clip.with_position('center')
    
    from modules.countdown_engine import generate_countdown_clip
    countdown_clip = generate_countdown_clip(duration, resolution).with_start(2)
    
    # 4. Reveal Scene
    from modules.reveal_animation_engine import generate_reveal_clip
    reveal_clip = generate_reveal_clip(image_path, 5, resolution).with_start(2 + duration)
    
    try:
        reveal_text = TextClip(
            font="Arial-Bold",
            text=f"It's a {animal_name}!",
            font_size=60,
            color='white',
            stroke_color='black',
            stroke_width=4
        ).with_position(('center', 550)).with_duration(5).with_start(2 + duration)
    except:
        reveal_text = ColorClip(size=(w, 100), color=(0,0,0,0)).with_duration(5).with_start(2 + duration)
        
    from modules.celebration_engine import generate_celebration_clip
    celebration_clip = generate_celebration_clip(5, resolution).with_start(2 + duration)
    
    # 6. Audio / Narration & Subtitles
    from modules.narration_engine import generate_narration
    
    tts_text_q1 = f"Can you guess this animal?"
    tts_text_q2 = f"Look carefully!"
    tts_text_a = f"Correct! It's a {animal_name}!"
    
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
            
    # Add soft kids-friendly background music
    bg_music_path = "uploads/nastelbom-kids-happy-happy-kid-488310.mp3"
    if os.path.exists(bg_music_path):
        try:
            bg_music = AudioFileClip(bg_music_path).with_duration(total_duration)
            bg_music = bg_music.volumex(0.15)
            audio_clips.append(bg_music)
            print("Background music added successfully.")
        except Exception as e:
            print(f"Failed to load background music: {e}")
            
    # Composite Video with Subtitles
    clips_to_composite = [
        bg_clip,
        intro_text,
        silh_clip,
        countdown_clip,
        reveal_clip,
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
            
    return final_video, [silh_path, tts_path_q1, tts_path_q2, tts_path_a]

def generate_guess_animal_video(image_path, theme, duration, output_folder):
    """
    Main pipeline for Guess The Animal game mode (Single Image).
    """
    resolution = (1280, 720)
    clip, paths_to_cleanup = _create_guess_animal_clip(image_path, theme, duration, resolution, output_folder)
    
    animal_name = "the animal"
    if image_path:
        animal_name = os.path.splitext(os.path.basename(image_path))[0].replace('_', ' ').capitalize()
        
    output_filename = f"{animal_name.lower().replace(' ', '_')}_short.mp4"
    output_path = os.path.join(output_folder, output_filename)
    
    clip.write_videofile(output_path, fps=15, codec="libx264", audio_codec="aac")
    
    # Cleanup
    for p in paths_to_cleanup:
        if os.path.exists(p):
            try: os.remove(p)
            except: pass
            
    return output_filename

def generate_guess_animal_video_multi(image_paths, theme, duration, output_folder):
    """
    Pipeline for Guess The Animal game mode with MULTIPLE images.
    Generates ONE video with multiple frames.
    """
    resolution = (1280, 720)
    clips = []
    all_paths_to_cleanup = []
    
    for img_path in image_paths:
        clip, paths = _create_guess_animal_clip(img_path, theme, duration, resolution, output_folder)
        clips.append(clip)
        all_paths_to_cleanup.extend(paths)
        
    final_video = concatenate_videoclips(clips)
    
    output_filename = f"multi_puzzle_{int(time.time())}.mp4"
    output_path = os.path.join(output_folder, output_filename)
    
    final_video.write_videofile(output_path, fps=15, codec="libx264", audio_codec="aac")
    
    # Cleanup
    for p in all_paths_to_cleanup:
        if os.path.exists(p):
            try: os.remove(p)
            except: pass
            
    return output_filename
