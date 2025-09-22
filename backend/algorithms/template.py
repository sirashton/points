"""
Template Algorithm
Copy this file and customize it for your own pointillism algorithm
"""

import io
import random
import numpy as np
from PIL import Image, ImageDraw

# Required metadata - CHANGE THESE
ALGORITHM_NAME = "My Algorithm Name"
ALGORITHM_DESCRIPTION = "Brief description of what your algorithm does"
ALGORITHM_AUTHOR = "Your Name"
ALGORITHM_VERSION = "1.0.0"

# Hide this algorithm from the UI (it's a template for developers)
ALGORITHM_HIDDEN = True

# Optional: Define custom parameters for the UI
# Remove this section if you don't need custom parameters
ALGORITHM_PARAMETERS = [
    {
        "name": "dot_size",
        "type": "slider",
        "label": "Dot Size",
        "min": 1,
        "max": 20,
        "default": 5,
        "description": "Size of the dots/strokes"
    },
    {
        "name": "dot_count",
        "type": "slider",
        "label": "Number of Dots",
        "min": 100,
        "max": 100000,
        "step": 100,
        "default": 1000,
        "description": "Number of dots/strokes to generate"
    },
    {
        "name": "intensity",
        "type": "slider",
        "label": "Color Intensity",
        "min": 0.5,
        "max": 2.0,
        "step": 0.1,
        "default": 1.2,
        "description": "How intense the colors should be"
    },
    {
        "name": "style",
        "type": "select",
        "label": "Artistic Style",
        "options": [
            {"value": "soft", "label": "Soft & Gentle"},
            {"value": "bold", "label": "Bold & Expressive"},
            {"value": "minimal", "label": "Minimal & Clean"}
        ],
        "default": "soft",
        "description": "Choose the artistic style"
    },
    {
        "name": "use_effect",
        "type": "checkbox",
        "label": "Apply Special Effect",
        "default": True,
        "description": "Add a special effect to the result"
    }
]

def create_pointillism(image_data, **custom_params):
    """
    Create pointillism art from image data
    
    Args:
        image_data (bytes): Raw image data from uploaded file
        **custom_params: Custom parameters defined in ALGORITHM_PARAMETERS
        
    Returns:
        PIL.Image: The processed pointillism image
        
    Raises:
        Exception: If processing fails
    """
    try:
        # Get custom parameters with defaults
        dot_size = custom_params.get('dot_size', 5)
        dot_count = custom_params.get('dot_count', 1000)
        intensity = custom_params.get('intensity', 1.2)
        style = custom_params.get('style', 'soft')
        use_effect = custom_params.get('use_effect', True)
        
        # Open image from bytes
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array
        img_array = np.array(image)
        height, width, channels = img_array.shape
        
        # Create result image
        result = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(result)
        
        # YOUR ALGORITHM LOGIC HERE
        # This is just a basic example - replace with your own logic
        
        for _ in range(dot_count):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            
            # Get original color
            original_color = img_array[y, x]
            
            # Apply intensity
            enhanced_color = tuple(np.clip(original_color * intensity, 0, 255).astype(int))
            
            # Adjust dot size based on style
            current_dot_size = dot_size
            if style == 'bold':
                current_dot_size = int(dot_size * 1.3)
            elif style == 'minimal':
                current_dot_size = int(dot_size * 0.7)
            
            # Draw dot
            left = x - current_dot_size
            top = y - current_dot_size
            right = x + current_dot_size
            bottom = y + current_dot_size
            draw.ellipse([left, top, right, bottom], fill=enhanced_color)
        
        # Apply special effect if enabled
        if use_effect:
            # Add your special effect here
            pass
        
        return result
        
    except Exception as e:
        # Always handle errors gracefully
        raise Exception(f"Algorithm failed: {str(e)}")

# Test your algorithm (optional)
if __name__ == "__main__":
    print("Testing algorithm...")
    
    # Load a test image
    try:
        with open("test_image.jpg", "rb") as f:
            image_data = f.read()
        
        # Test basic functionality
        result = create_pointillism(image_data)
        result.save("test_output.png")
        print("✅ Basic test completed!")
        
        # Test with custom parameters
        custom_params = {
            'dot_size': 5,
            'dot_count': 1000,
            'intensity': 1.5,
            'style': 'bold',
            'use_effect': True
        }
        
        result = create_pointillism(image_data, **custom_params)
        result.save("test_output_custom.png")
        print("✅ Custom parameters test completed!")
        
    except FileNotFoundError:
        print("⚠️  No test image found. Create a 'test_image.jpg' file to test your algorithm.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
