# Algorithm Plugin System

This directory contains pointillism algorithms that can be dynamically loaded by the Pointillism Generator web application. The system supports a plugin architecture where developers can add new algorithms by simply dropping a Python file into this folder.

## 🚀 Quick Start

1. **Create a new Python file** in this directory (e.g., `my_algorithm.py`)
2. **Copy the template below** and customize it
3. **Restart the application** - your algorithm will automatically appear in the web interface!

## 📁 File Structure

```
backend/algorithms/
├── __init__.py              # Plugin system core (don't modify)
├── README.md                # This documentation
├── simple.py                # Simple Dots algorithm
├── enhanced.py              # Enhanced Dots algorithm
├── original.py              # Original Strokes algorithm
├── ronchetti.py             # Ronchetti Original algorithm
├── watercolor.py            # Watercolor example with custom parameters
├── impressionist.py         # Impressionist example with advanced parameters
└── your_algorithm.py        # Your new algorithm (create this)
```

## 🎯 How to Add a New Algorithm

### 1. Create Your Algorithm File

Create a new Python file in this directory with the following naming convention:
- File name: `{algorithm_name}.py` (lowercase, underscores)
- Example: `watercolor.py`, `impressionist.py`, `cubist.py`, `my_awesome_algorithm.py`

### 2. Required File Structure

Your algorithm file must contain:

```python
# Required metadata at the top of the file
ALGORITHM_NAME = "Your Algorithm Name"
ALGORITHM_DESCRIPTION = "Brief description of what your algorithm does"
ALGORITHM_AUTHOR = "Your Name"
ALGORITHM_VERSION = "1.0.0"

# Optional: Define custom parameters for the UI
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
        "name": "brush_size",
        "type": "slider",
        "label": "Brush Size",
        "min": 1,
        "max": 20,
        "default": 5,
        "description": "Size of the brush strokes"
    },
    {
        "name": "color_intensity",
        "type": "slider", 
        "label": "Color Intensity",
        "min": 0.1,
        "max": 2.0,
        "step": 0.1,
        "default": 1.0,
        "description": "Intensity of colors"
    },
    {
        "name": "style",
        "type": "select",
        "label": "Art Style",
        "options": [
            {"value": "impressionist", "label": "Impressionist"},
            {"value": "expressionist", "label": "Expressionist"},
            {"value": "realist", "label": "Realist"}
        ],
        "default": "impressionist",
        "description": "Choose the artistic style"
    },
    {
        "name": "use_gradients",
        "type": "checkbox",
        "label": "Use Gradients",
        "default": True,
        "description": "Apply gradient effects"
    }
]

def create_pointillism(image_data, **custom_params):
    """
    Create pointillism art from image data
    
    Args:
        image_data (bytes): Raw image data from uploaded file
        **custom_params: Custom parameters defined in ALGORITHM_PARAMETERS
                       May include 'dot_size' and 'dot_count' if algorithm requests them
        
    Returns:
        PIL.Image: The processed pointillism image
        
    Raises:
        Exception: If processing fails
    """
    # Your algorithm implementation here
    pass
```

### 3. Complete Examples

#### Basic Algorithm (No Custom Parameters)
```python
"""
Basic Pointillism Algorithm
Simple example without custom parameters
"""

import io
import random
import numpy as np
from PIL import Image, ImageDraw

# Required metadata
ALGORITHM_NAME = "My Basic Algorithm"
ALGORITHM_DESCRIPTION = "A simple pointillism algorithm"
ALGORITHM_AUTHOR = "Your Name"
ALGORITHM_VERSION = "1.0.0"

def create_pointillism(image_data, **custom_params):
    """
    Create basic pointillism art
    """
    # Get parameters with defaults
    dot_size = custom_params.get('dot_size', 5)
    dot_count = custom_params.get('dot_count', 1000)
    
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
    
    # Generate random dots
    for _ in range(dot_count):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        color = tuple(img_array[y, x])
        
        # Draw circular dot
        left = x - dot_size
        top = y - dot_size
        right = x + dot_size
        bottom = y + dot_size
        draw.ellipse([left, top, right, bottom], fill=color)
    
    return result
```

#### Advanced Algorithm (With Custom Parameters)
```python
"""
Advanced Pointillism Algorithm
Example with custom parameters and UI controls
"""

import io
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from sklearn.cluster import KMeans

# Required metadata
ALGORITHM_NAME = "My Advanced Algorithm"
ALGORITHM_DESCRIPTION = "Advanced pointillism with custom controls"
ALGORITHM_AUTHOR = "Your Name"
ALGORITHM_VERSION = "1.0.0"

# Custom parameters for the UI
ALGORITHM_PARAMETERS = [
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
        "name": "use_blur",
        "type": "checkbox",
        "label": "Apply Blur Effect",
        "default": True,
        "description": "Add a subtle blur effect"
    }
]

def create_pointillism(image_data, **custom_params):
    """
    Create advanced pointillism art with custom parameters
    """
    # Get custom parameters
    dot_size = custom_params.get('dot_size', 5)
    dot_count = custom_params.get('dot_count', 1000)
    intensity = custom_params.get('intensity', 1.2)
    style = custom_params.get('style', 'soft')
    use_blur = custom_params.get('use_blur', True)
    
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
    
    # Generate dots with custom styling
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
    
    # Apply blur if enabled
    if use_blur:
        result = result.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return result
```

### 4. Real Examples

- **`watercolor.py`** - Watercolor effects with 4 custom parameters
- **`impressionist.py`** - Impressionist styles with 5 custom parameters
- **`simple.py`** - Basic algorithm without custom parameters

### 5. Available Imports

You can use these packages in your algorithm:

```python
# Standard library
import io
import random
import math

# Third-party packages (already installed)
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from sklearn.cluster import KMeans
import cv2
```

### 6. Parameter Types Reference

| **Type** | **Description** | **Required Fields** | **Optional Fields** |
|----------|-----------------|---------------------|---------------------|
| **slider** | Numeric range input | `name`, `type`, `label`, `min`, `max`, `default` | `step`, `description` |
| **select** | Dropdown selection | `name`, `type`, `label`, `options`, `default` | `description` |
| **checkbox** | Boolean toggle | `name`, `type`, `label`, `default` | `description` |

#### Slider Example:
```python
{
    "name": "blur_radius",
    "type": "slider",
    "label": "Blur Radius",
    "min": 0.1,
    "max": 2.0,
    "step": 0.1,
    "default": 0.5,
    "description": "Amount of blur effect"
}
```

#### Select Example:
```python
{
    "name": "art_style",
    "type": "select",
    "label": "Art Style",
    "options": [
        {"value": "impressionist", "label": "Impressionist"},
        {"value": "expressionist", "label": "Expressionist"}
    ],
    "default": "impressionist",
    "description": "Choose the artistic style"
}
```

#### Checkbox Example:
```python
{
    "name": "use_texture",
    "type": "checkbox",
    "label": "Add Texture",
    "default": True,
    "description": "Apply texture effects"
}
```

### 7. Best Practices

#### Performance
- Keep processing time under 30 seconds for typical images
- Use efficient algorithms for large images
- Consider image size when determining stroke count

#### Quality
- Ensure consistent output quality across different images
- Handle edge cases (very small/large images, unusual aspect ratios)
- Provide meaningful error messages

#### Compatibility
- Always return a PIL.Image object
- Handle different image formats gracefully
- Ensure the result image matches input dimensions

#### Parameter Design
- Use descriptive names and labels
- Provide helpful descriptions
- Choose appropriate min/max values for sliders
- Use meaningful option labels for selects

### 8. Testing Your Algorithm

```python
# Test script (optional)
if __name__ == "__main__":
    # Load test image
    with open("test_image.jpg", "rb") as f:
        image_data = f.read()
    
    # Test basic functionality
    result = create_pointillism(image_data, dot_size=5, dot_count=1000)
    result.save("test_output.png")
    print("Basic test completed!")
    
    # Test with custom parameters (if applicable)
    if 'ALGORITHM_PARAMETERS' in globals():
        custom_params = {}
        for param in ALGORITHM_PARAMETERS:
            custom_params[param['name']] = param['default']
        
        result = create_pointillism(image_data, dot_size=5, dot_count=1000, **custom_params)
        result.save("test_output_custom.png")
        print("Custom parameters test completed!")
```

### 9. Algorithm Registration

The system automatically:
1. Scans this directory for `.py` files
2. Imports each file and extracts metadata
3. Registers the algorithm in the web interface
4. Makes it available in the dropdown menu
5. Generates UI controls for custom parameters

### 10. Frontend Integration

Your algorithm will automatically appear in the web interface with:
- **Display Name**: From `ALGORITHM_NAME`
- **Description**: From `ALGORITHM_DESCRIPTION`
- **Author**: From `ALGORITHM_AUTHOR`
- **Custom Controls**: Generated from `ALGORITHM_PARAMETERS`

### 11. Troubleshooting

If your algorithm doesn't appear in the web interface:

1. **Check file location**: Ensure your file is in `backend/algorithms/` directory
2. **Verify metadata**: Make sure all required metadata variables exist
3. **Check function**: Ensure `create_pointillism` function exists
4. **Syntax errors**: Run your file with `python your_algorithm.py` to check for errors
5. **Backend logs**: Check Docker logs with `docker-compose logs backend`
6. **Parameter format**: Ensure `ALGORITHM_PARAMETERS` follows the correct format

### 12. Common Issues

| **Issue** | **Solution** |
|-----------|--------------|
| Algorithm not appearing | Check file is in correct directory and has required metadata |
| Parameter controls not showing | Verify `ALGORITHM_PARAMETERS` format is correct |
| Import errors | Ensure all imports are available in the Docker environment |
| Processing errors | Check that function returns PIL.Image object |
| Parameter not working | Verify parameter name matches in function signature |

### 13. Need Help?

- **Examples**: Check `watercolor.py` and `impressionist.py` for complete examples
- **Logs**: Use `docker-compose logs backend` to see error messages
- **Testing**: Test your algorithm independently before deploying
- **Documentation**: This README contains all the information you need

## 🎨 Current Algorithms

- **Simple Dots** - Basic uniform circular dots
- **Enhanced Dots** - Smart color palette with limited size variation
- **Original Strokes** - Brush strokes with adaptive density
- **Ronchetti Original** - Matteo Ronchetti's adaptive approach
- **Watercolor** - Soft, flowing watercolor effects (4 custom parameters)
- **Impressionist** - Impressionist styles with artistic controls (5 custom parameters)

## 🚀 Ready to Submit?

Once you've created your algorithm:

1. **Test it thoroughly** with different images
2. **Check the logs** for any errors
3. **Verify the UI** shows your custom parameters correctly
4. **Submit your file** to the project maintainers

Your algorithm will be automatically integrated into the web application! 🎨✨