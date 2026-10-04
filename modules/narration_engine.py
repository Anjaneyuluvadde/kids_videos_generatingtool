import os
import pyttsx3
import time
from modules.story_generator import detect_image_category, generate_story

def generate_narration(text, output_path, image_path=None, voice_name=None):
    """
    Generates speech using pyttsx3 (offline TTS).
    Saves to output_path.
    Now supports image detection and voice selection.
    """
    print(f"--- Narration Generation Status: Starting ---")
    
    # Task 1: Fix Uploaded Image Detection
    if image_path:
        print(f"Image path provided: {image_path}")
        if not os.path.exists(image_path):
            print(f"Error: Image not found at {image_path}")
            image_path = None
        else:
            print(f"Image validated successfully.")
            
    # Task 5 & 7: Improve Narration Pipeline / Better AI Image Detection
    if image_path and (not text or text == "Hello"):
        print("Detecting object from image...")
        category = detect_image_category(image_path)
        print(f"Detected category: {category}")
        text = generate_story(category)
        print(f"Generated Narration Text: {text}")
        
    print(f"Final Narration Text: {text}")
    print(f"Requested Voice: {voice_name}")

    try:
        engine = pyttsx3.init()
        
        # Task 3: Add Voice Detection Debugging
        voices = engine.getProperty('voices')
        print("Available System Voices:")
        for idx, v in enumerate(voices):
            print(f"  [{idx}] Name: {v.name}, ID: {v.id}")
            
        # Task 2: Fix Multiple Voice Support
        selected_voice = None
        
        # Mapping
        voice_keywords = {
            "Joyful Boy": ["male", "david", "boy"],
            "Sweet Girl": ["female", "zira", "girl"],
            "Miss Teacher": ["female", "zira", "teacher"]
        }
        
        if voice_name in voice_keywords:
            keywords = voice_keywords[voice_name]
            for v in voices:
                v_name_lower = v.name.lower()
                if any(kw in v_name_lower for kw in keywords):
                    selected_voice = v
                    break
                    
        # Fallback if requested voice not found or not specified
        if not selected_voice and voices:
            print(f"Warning: Voice '{voice_name}' not found or unavailable. Using fallback.")
            if voice_name in ["Sweet Girl", "Miss Teacher"]:
                for v in voices:
                    if "female" in v.name.lower() or "zira" in v.name.lower():
                        selected_voice = v
                        break
            elif voice_name == "Joyful Boy":
                for v in voices:
                    if "male" in v.name.lower() or "david" in v.name.lower():
                        selected_voice = v
                        break
                        
            if not selected_voice:
                selected_voice = voices[0]
                
        if selected_voice:
            print(f"Selected Voice: {selected_voice.name}")
            engine.setProperty('voice', selected_voice.id)
        else:
            print("Warning: No voices found on system!")

        engine.setProperty('rate', 160)
        engine.setProperty('volume', 1.0)
        
        # Task 4: Improve Voice Stability
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Audio file successfully generated at {output_path}")
            print(f"--- Narration Generation Status: Success ---")
            return output_path
        else:
            print(f"Error: Failed to generate audio file or file is empty.")
            print(f"--- Narration Generation Status: Failed ---")
            return None
            
    except Exception as e:
        print(f"TTS failed: {e}")
        print(f"--- Narration Generation Status: Failed with Exception ---")
        return None

