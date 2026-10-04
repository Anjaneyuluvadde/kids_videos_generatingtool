import os
import random
from moviepy import ImageClip, TextClip, CompositeVideoClip, ColorClip

def generate_puzzle(puzzle_type, image_path, theme, duration):
    """
    Core engine to dispatch to specific puzzle generators based on type.
    """
    if puzzle_type == 'guess_animal':
        return _guess_animal(image_path, theme, duration)
    elif puzzle_type == 'hidden_object':
        return _hidden_object(image_path, theme, duration)
    elif puzzle_type == 'emoji_puzzle':
        return _emoji_puzzle(theme, duration)
    elif puzzle_type == 'spot_difference':
        return _spot_difference(image_path, theme, duration)
    elif puzzle_type == 'memory_game':
        return _memory_game(image_path, theme, duration)
    elif puzzle_type == 'shape_matching':
        return _shape_matching(image_path, theme, duration)
    elif puzzle_type == 'color_matching':
        return _color_matching(image_path, theme, duration)
    else:
        raise ValueError(f"Unknown puzzle type: {puzzle_type}")

def _guess_animal(image_path, theme, duration):
    texts = [
        "Can you guess the animal?",
        "Who is hiding here?",
        "Guess the animal!"
    ]
    animal_name = "the animal"
    if image_path:
        animal_name = os.path.splitext(os.path.basename(image_path))[0]
        animal_name = animal_name.replace('_', ' ').capitalize()
        
    return {
        "type": "guess_animal", 
        "image": image_path, 
        "theme": theme, 
        "duration": duration, 
        "text": random.choice(texts),
        "answer": f"Excellent, it's {animal_name}!"
    }

def _hidden_object(image_path, theme, duration):
    return {"type": "hidden_object", "image": image_path, "theme": theme, "duration": duration, "text": "Find the hidden object!"}

def _emoji_puzzle(theme, duration):
    return {"type": "emoji_puzzle", "image": None, "theme": theme, "duration": duration, "text": "Guess the Emoji!"}

def _spot_difference(image_path, theme, duration):
    return {"type": "spot_difference", "image": image_path, "theme": theme, "duration": duration, "text": "Spot the Difference!"}

def _memory_game(image_path, theme, duration):
    return {"type": "memory_game", "image": image_path, "theme": theme, "duration": duration, "text": "Memory Game!"}

def _shape_matching(image_path, theme, duration):
    return {"type": "shape_matching", "image": image_path, "theme": theme, "duration": duration, "text": "Match the Shapes!"}

def _color_matching(image_path, theme, duration):
    return {"type": "color_matching", "image": image_path, "theme": theme, "duration": duration, "text": "Match the Colors!"}
