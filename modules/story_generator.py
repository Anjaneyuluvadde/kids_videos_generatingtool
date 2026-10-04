import os
import random

_classifier = None

def get_classifier():
    global _classifier
    if _classifier is not None:
        return _classifier
        
    try:
        from transformers import pipeline
        print("Loading image classification model (may take a moment)...")
        _classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
        print("Model loaded successfully!")
        return _classifier
    except Exception as e:
        print("Warning: Could not load transformers or model. Using fallback simulation.", e)
        _classifier = False
        return None

def detect_image_category(image_path):
    # Task 1 & 7: Improve path handling
    if not image_path or not os.path.exists(image_path):
        print(f"Image path invalid or not found: {image_path}")
        return "unknown"
        
    classifier = get_classifier()
    if classifier:
        try:
            result = classifier(image_path)
            full_label = result[0]['label'].lower()
            
            # Simple keyword matching for kids categories
            if 'cat' in full_label or 'tiger' in full_label or 'lion' in full_label:
                return 'lion' if 'lion' in full_label else 'cat'
            if 'dog' in full_label or 'puppy' in full_label:
                return 'dog'
            if 'car' in full_label or 'vehicle' in full_label:
                return 'car'
            if 'ball' in full_label or 'sports' in full_label:
                return 'ball'
            if 'elephant' in full_label:
                return 'elephant'
                
            return full_label.split(',')[0]
        except Exception as e:
            print("Classification error:", e)
    
    # Fallback simulation
    categories = ["cat", "dog", "car", "ball", "lion", "elephant"]
    return random.choice(categories)

def generate_story(category):
    # Task 7: Improve narration text generation
    stories = {
        "lion": "Leo the Lion loves running in the jungle! Roar!",
        "cat": "The fluffy cat is playing with a colorful ball of yarn.",
        "car": "Zoom zoom! The fast car wins the big race!",
        "ball": "Bounce, bounce! The red ball jumps over the fence.",
        "dog": "Happy puppy chasing its tail in the sunny park!",
        "elephant": "The big elephant is spraying water with its trunk!",
        "unknown": "Look at this amazing picture! It's having a wonderful day!"
    }
    
    for key, story in stories.items():
        if key in category:
            return story
            
    return f"Look at this amazing {category}! It's having a wonderful day!"

