def get_sound_effect(category):
    """
    Returns a dummy sound effect track or paths.
    In a fully featured app, this would return actual .mp3 paths from an assets folder.
    """
    effects = {
        "pop": "assets/sounds/pop_sound.mp3",
        "animal": "assets/sounds/animal_sound.mp3",
        "car": "assets/sounds/vroom.mp3",
        "kids": "assets/sounds/kids_cheer.mp3"
    }
    
    if "car" in category:
        return effects["car"]
    elif "lion" in category or "dog" in category or "cat" in category:
        return effects["animal"]
    else:
        return effects["kids"]
