import os
import time
from moviepy import ImageClip, TextClip, CompositeVideoClip, ColorClip, AudioFileClip
from modules.background_generator import generate_background
from modules.timer_engine import generate_timer_clip
from modules.narration_engine import generate_narration

def render_puzzle_video(puzzle_data, output_folder, resolution=(1280, 720)):
    """
    Renders the final puzzle video.
    Forced to 16:9 ratio (1280x720).
    """
    duration = puzzle_data.get('duration', 10)
    w, h = resolution
    
    # 1. Visual Theme (Background)
    theme = puzzle_data.get('theme', 'jungle')
    bg_array = generate_background(theme=theme, width=w, height=h)
    bg_clip = ImageClip(bg_array).with_duration(duration)
    
    clips_to_composite = [bg_clip]
    
    # 2. Challenge Timer
    timer_clip = generate_timer_clip(duration, (w, h))
    clips_to_composite.append(timer_clip)
    
    # Add Image if present
    if puzzle_data.get('image') and os.path.exists(puzzle_data['image']):
        try:
            img_clip = ImageClip(puzzle_data['image'])
            
            # Resize logic (keep aspect ratio)
            img_w, img_h = img_clip.size
            scale = min((w * 0.8) / img_w, (h * 0.5) / img_h)
            img_clip = img_clip.resized(new_size=(int(img_w * scale), int(img_h * scale)))
            
            # Position at center
            img_clip = img_clip.with_position('center').with_duration(duration)
            clips_to_composite.append(img_clip)
        except Exception as e:
            print(f"Error loading image: {e}")

    # Add Text
    if puzzle_data.get('text'):
        try:
            # Question Clip (0 to duration - 3)
            q_clip = TextClip(
                font="Arial-Bold", 
                text=puzzle_data['text'], 
                font_size=60, 
                color='yellow', 
                stroke_color='black', 
                stroke_width=4
            ).with_position(('center', 100)).with_duration(duration - 3)
            clips_to_composite.append(q_clip)
            
            # Answer Clip (duration - 3 to duration)
            if puzzle_data.get('answer'):
                a_clip = TextClip(
                    font="Arial-Bold", 
                    text=puzzle_data['answer'], 
                    font_size=60, 
                    color='white', 
                    stroke_color='black', 
                    stroke_width=4
                ).with_position(('center', 100)).with_duration(3).with_start(duration - 3)
                clips_to_composite.append(a_clip)
                
        except Exception as e:
            print("TextClip failed. Install ImageMagick to fix this:", e)
            
    final_video = CompositeVideoClip(clips_to_composite)
    
    # 3. AI Voice Actor (Narration)
    tts_text_q = puzzle_data.get('text', 'Hello')
    tts_text_a = puzzle_data.get('answer')
    
    tts_path_q = os.path.join(output_folder, f"tts_q_{int(time.time())}.mp3")
    tts_path_a = os.path.join(output_folder, f"tts_a_{int(time.time())}.mp3")
    
    generate_narration(tts_text_q, tts_path_q)
    if tts_text_a:
        generate_narration(tts_text_a, tts_path_a)
        
    audio_clips = []
    
    if os.path.exists(tts_path_q):
        try:
            audio_q = AudioFileClip(tts_path_q).with_start(0)
            audio_clips.append(audio_q)
        except Exception as e:
            print(f"Failed to load audio Q: {e}")
            
    if tts_text_a and os.path.exists(tts_path_a):
        try:
            audio_a = AudioFileClip(tts_path_a).with_start(duration - 3)
            audio_clips.append(audio_a)
        except Exception as e:
            print(f"Failed to load audio A: {e}")
            
    # Add soft kids-friendly background music
    bg_music_path = "uploads/nastelbom-kids-happy-happy-kid-488310.mp3"
    if os.path.exists(bg_music_path):
        try:
            bg_music = AudioFileClip(bg_music_path).with_duration(duration)
            bg_music = bg_music.volumex(0.15)
            audio_clips.append(bg_music)
            print("Background music added successfully.")
        except Exception as e:
            print(f"Failed to load background music: {e}")
            
    if audio_clips:
        try:
            from moviepy import CompositeAudioClip
            final_audio = CompositeAudioClip(audio_clips)
            final_video = final_video.with_audio(final_audio)
        except Exception as e:
            print(f"Failed to composite audio: {e}")
            
    os.makedirs(output_folder, exist_ok=True)
    output_filename = f"{puzzle_data.get('type', 'puzzle')}_{int(time.time())}.mp4"
    output_path = os.path.join(output_folder, output_filename)
    
    # Write file
    final_video.write_videofile(output_path, fps=10, codec="libx264", audio_codec="aac")
    
    # Clean up temp audio file
    if os.path.exists(tts_path_q):
        try: os.remove(tts_path_q) 
        except: pass
    if os.path.exists(tts_path_a):
        try: os.remove(tts_path_a) 
        except: pass
            
    return output_filename
