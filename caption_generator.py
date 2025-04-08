# caption_generator.py
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Load BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def generate_caption(image: Image.Image) -> str:
    """
    Generate an image caption using the BLIP model.

    Args:
        image (PIL.Image.Image): Input image

    Returns:
        str: Generated caption
    """
    image = image.convert("RGB")  # Ensure it's in RGB format
    inputs = processor(images=image, return_tensors="pt").to(device)
    out = model.generate(**inputs, max_length=50)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption
