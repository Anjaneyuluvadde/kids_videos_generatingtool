from PIL import Image, ImageFilter
import os

def generate_silhouette(image_path, output_path):
    """
    Creates a blurred/silhouette version of the animal image using Pillow.
    """
    try:
        img = Image.open(image_path)
        # Apply a strong Gaussian blur to hide the animal details
        blurred = img.filter(ImageFilter.GaussianBlur(radius=30))
        blurred.save(output_path)
        return output_path
    except Exception as e:
        print(f"Silhouette generation failed: {e}")
        return image_path # Fallback to original if failed
