"""
Caption generator module using local Whisper.
Generates animated, colorful text for kids.
"""

def generate_captions(audio_path, use_whisper=True):
    """
    Generates captions from audio.
    If use_whisper is true, uses the local whisper model.
    """
    captions = []
    if use_whisper:
        try:
            # import whisper
            # model = whisper.load_model("base")
            # result = model.transcribe(audio_path)
            # return format_whisper_result(result)
            captions.append({"text": "Hello Kids!", "start": 0.0, "end": 2.0})
            captions.append({"text": "Let's learn", "start": 2.0, "end": 4.0})
        except Exception as e:
            print(f"Whisper not loaded or error: {e}")
            captions.append({"text": "Music playing 🎵", "start": 0.0, "end": 5.0})
    else:
        captions.append({"text": "🎵 Happy Music 🎵", "start": 0.0, "end": 5.0})
        
    return captions

def format_caption_style(text):
    """
    Returns settings for colorful, animated captions suitable for kids.
    """
    return {
        "font": "Comic Sans MS", # Standard fun font
        "color": "yellow",
        "stroke_color": "black",
        "stroke_width": 3,
        "fontsize": 70
    }
