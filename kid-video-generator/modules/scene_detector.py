"""
Scene detection module for the Kid Video Generator.
Handles timing of image/video appearances.
"""

def detect_scenes(visual_assets):
    """
    Analyzes visual assets and determines optimal scene durations.
    """
    scenes = []
    for asset in visual_assets:
        scenes.append({
            "asset": asset,
            "duration": 3.0, # Default 3 seconds per scene
            "transition": "crossfade"
        })
    return scenes
