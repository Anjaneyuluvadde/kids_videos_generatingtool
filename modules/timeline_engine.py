def build_timeline(duration=10):
    """
    Builds a timeline dictionary for a kids story video.
    Breaks down the requested duration into an intro, main body, and outro.
    """
    intro_dur = min(2.0, duration * 0.2)
    outro_dur = min(2.0, duration * 0.2)
    main_dur = duration - intro_dur - outro_dur
    
    return {
        "intro": {"start": 0, "end": intro_dur, "effect": "fadein"},
        "main": {"start": intro_dur, "end": intro_dur + main_dur, "effect": "zoom_pan"},
        "outro": {"start": intro_dur + main_dur, "end": duration, "effect": "fadeout"}
    }
