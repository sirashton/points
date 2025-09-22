"""
Simple Dots Algorithm
Basic uniform circular dots pointillism
"""

import io
import random
import numpy as np
from PIL import Image, ImageDraw

# Required metadata
ALGORITHM_NAME = "Simple Dots"
ALGORITHM_DESCRIPTION = "Basic uniform circular dots"
ALGORITHM_AUTHOR = "Pointillism Generator"
ALGORITHM_VERSION = "1.0.0"

# Custom parameters for the UI
ALGORITHM_PARAMETERS = [
    {
        "name": "dot_size",
        "type": "slider",
        "label": "Dot Size",
        "min": 1,
        "max": 20,
        "default": 5,
        "description": "Size of the dots"
    },
    {
        "name": "dot_count",
        "type": "slider",
        "label": "Number of Dots",
        "min": 100,
        "max": 100000,
        "step": 100,
        "default": 1000,
        "description": "Number of dots to generate"
    }
]

def create_pointillism(image_data, **custom_params):
    """
    Create simple pointillism with uniform circular dots
    """
    # Get parameters with defaults
    dot_size = custom_params.get('dot_size', 5)
    dot_count = custom_params.get('dot_count', 1000)
    
    # Open image from bytes
    image = Image.open(io.BytesIO(image_data))
    
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert to numpy array for processing
    img_array = np.array(image)
    height, width, channels = img_array.shape
    
    # Create result image
    result = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(result)
    
    # Generate random positions and colors
    for _ in range(dot_count):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        
        # Get color from original image
        color = tuple(img_array[y, x])
        
        # Draw circular dot
        left = x - dot_size
        top = y - dot_size
        right = x + dot_size
        bottom = y + dot_size
        
        draw.ellipse([left, top, right, bottom], fill=color)
    
    return result
