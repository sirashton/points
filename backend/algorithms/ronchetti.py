"""
Matteo Ronchetti's Pointillism Algorithm
Advanced pointillism with gradient-based stroke direction and intelligent color selection
Based on: https://medium.com/@matteoronchetti/https-medium-com-matteoronchetti-pointillism-with-python-and-opencv-f4274e6bbb7b
"""

import io
import math
import random
import bisect
import numpy as np
import cv2
from PIL import Image, ImageDraw
from sklearn.cluster import KMeans
import scipy.spatial.distance

# Required metadata
ALGORITHM_NAME = "Ronchetti Original"
ALGORITHM_DESCRIPTION = "Advanced pointillism with gradient-based stroke direction and intelligent color selection"
ALGORITHM_AUTHOR = "Matteo Ronchetti (adapted)"
ALGORITHM_VERSION = "1.0.0"

# Custom parameters for the UI
ALGORITHM_PARAMETERS = [
    {
        "name": "palette_size",
        "type": "slider",
        "label": "Color Palette Size",
        "min": 5,
        "max": 50,
        "default": 20,
        "description": "Number of colors in the base palette"
    },
    {
        "name": "stroke_scale",
        "type": "slider",
        "label": "Stroke Scale",
        "min": 1,
        "max": 20,
        "default": 0,
        "description": "Scale of brush strokes (0 = automatic)"
    },
    {
        "name": "gradient_smoothing",
        "type": "slider",
        "label": "Gradient Smoothing",
        "min": 0,
        "max": 20,
        "default": 0,
        "description": "Gradient smoothing radius (0 = automatic)"
    },
    {
        "name": "grid_scale",
        "type": "slider",
        "label": "Grid Density",
        "min": 1,
        "max": 10,
        "default": 3,
        "description": "Density of the stroke grid"
    },
    {
        "name": "color_randomness",
        "type": "slider",
        "label": "Color Randomness",
        "min": 1,
        "max": 20,
        "default": 9,
        "description": "Lower values = more randomness in color selection"
    },
    {
        "name": "use_median_blur",
        "type": "checkbox",
        "label": "Apply Median Blur",
        "default": True,
        "description": "Apply median blur for a more painted look"
    }
]

def limit_size(img, max_size):
    """Limit image size while maintaining aspect ratio"""
    if max_size == 0:
        return img
    
    h, w = img.shape[:2]
    ratio = min(1.0, float(max_size) / max(h, w))
    
    if ratio != 1.0:
        new_w = int(w * ratio)
        new_h = int(h * ratio)
        return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return img

def regulate(img, hue=0, saturation=0, luminosity=0):
    """Adjust HSV values of an image"""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
    if hue < 0:
        hue = 255 + hue
    hsv[:, :, 0] += hue
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] + saturation, 0, 255)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] + luminosity, 0, 255)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR_FULL)

class ColorPalette:
    """Color palette with K-means clustering and extension capabilities"""
    
    def __init__(self, colors, base_len=0):
        self.colors = colors
        self.base_len = base_len if base_len > 0 else len(colors)
    
    @staticmethod
    def from_image(img, n, max_img_size=200, n_init=10):
        """Create color palette from image using K-means clustering"""
        # Scale down image for faster clustering
        img_scaled = limit_size(img, max_img_size)
        
        # Reshape image for clustering
        data = img_scaled.reshape(-1, 3)
        
        # Apply K-means clustering
        clt = KMeans(n_clusters=n, n_init=n_init, random_state=42)
        clt.fit(data)
        
        return ColorPalette(clt.cluster_centers_)
    
    def extend(self, extensions):
        """Extend palette with additional color variations"""
        # Start with original colors
        extended_colors = [self.colors.astype(np.uint8)]
        
        for hue, sat, lum in extensions:
            # Reshape to 3D for regulate function, then back to 2D
            colors_3d = self.colors.reshape((1, len(self.colors), 3)).astype(np.uint8)
            extended = regulate(colors_3d, hue, sat, lum).reshape((-1, 3))
            extended_colors.append(extended)
        
        all_colors = np.vstack(extended_colors)
        return ColorPalette(all_colors, self.base_len)
    
    def __len__(self):
        return len(self.colors)
    
    def __getitem__(self, item):
        return self.colors[item]

class VectorField:
    """Vector field for gradient-based stroke direction"""
    
    def __init__(self, fieldx, fieldy):
        self.fieldx = fieldx
        self.fieldy = fieldy
    
    @staticmethod
    def from_gradient(gray):
        """Create vector field from image gradient using Scharr operators"""
        fieldx = cv2.Scharr(gray, cv2.CV_32F, 1, 0) / 15.36
        fieldy = cv2.Scharr(gray, cv2.CV_32F, 0, 1) / 15.36
        return VectorField(fieldx, fieldy)
    
    def smooth(self, radius, iterations=1):
        """Smooth the vector field using Gaussian blur"""
        s = 2 * radius + 1
        for _ in range(iterations):
            self.fieldx = cv2.GaussianBlur(self.fieldx, (s, s), 0)
            self.fieldy = cv2.GaussianBlur(self.fieldy, (s, s), 0)
    
    def direction(self, i, j):
        """Get gradient direction at position (i, j)"""
        return math.atan2(self.fieldy[i, j], self.fieldx[i, j])
    
    def magnitude(self, i, j):
        """Get gradient magnitude at position (i, j)"""
        return math.hypot(self.fieldx[i, j], self.fieldy[i, j])

def compute_color_probabilities(pixels, palette, k=9):
    """Compute color selection probabilities based on distance to palette colors"""
    distances = scipy.spatial.distance.cdist(pixels, palette.colors)
    maxima = np.amax(distances, axis=1)
    
    # Normalize distances
    distances = maxima[:, None] - distances
    summ = np.sum(distances, 1)
    distances /= summ[:, None]
    
    # Apply exponential scaling for probability distribution
    distances = np.exp(k * len(palette) * distances)
    summ = np.sum(distances, 1)
    distances /= summ[:, None]
    
    return np.cumsum(distances, axis=1, dtype=np.float32)

def color_select(probabilities, palette):
    """Select color based on probability distribution"""
    r = random.uniform(0, 1)
    i = bisect.bisect_left(probabilities, r)
    return palette[i] if i < len(palette) else palette[-1]

def randomized_grid(h, w, scale):
    """Create randomized grid of stroke positions"""
    assert scale > 0
    
    r = scale // 2
    grid = []
    
    for i in range(0, h, scale):
        for j in range(0, w, scale):
            y = random.randint(-r, r) + i
            x = random.randint(-r, r) + j
            grid.append((y % h, x % w))
    
    random.shuffle(grid)
    return grid

def create_pointillism(image_data, **custom_params):
    """
    Create pointillism art using Matteo Ronchetti's algorithm
    
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
        palette_size = custom_params.get('palette_size', 20)
        stroke_scale = custom_params.get('stroke_scale', 0)
        gradient_smoothing = custom_params.get('gradient_smoothing', 0)
        grid_scale = custom_params.get('grid_scale', 3)
        color_randomness = custom_params.get('color_randomness', 9)
        use_median_blur = custom_params.get('use_median_blur', True)
        
        # Open image from bytes and convert to OpenCV format
        pil_image = Image.open(io.BytesIO(image_data))
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Convert PIL to OpenCV format (BGR)
        img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        height, width = img.shape[:2]
        
        # Auto-calculate stroke scale if not provided
        if stroke_scale == 0:
            stroke_scale = int(math.ceil(max(height, width) / 1000))
        
        # Auto-calculate gradient smoothing if not provided
        if gradient_smoothing == 0:
            gradient_smoothing = int(round(max(height, width) / 50))
        
        # Convert to grayscale for gradient computation
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Create color palette using K-means clustering
        palette = ColorPalette.from_image(img, palette_size)
        
        # Extend palette with additional color variations
        palette = palette.extend([(0, 50, 0), (15, 30, 0), (-15, 30, 0)])
        
        # Compute gradient vector field
        gradient = VectorField.from_gradient(gray)
        gradient.smooth(gradient_smoothing)
        
        # Create base image (optionally with median blur for painted look)
        if use_median_blur:
            result = cv2.medianBlur(img, 11)
        else:
            result = img.copy()
        
        # Create randomized grid of stroke positions
        grid = randomized_grid(height, width, scale=grid_scale)
        
        # Process strokes in batches for memory efficiency
        batch_size = 10000
        
        for h in range(0, len(grid), batch_size):
            batch_end = min(h + batch_size, len(grid))
            batch_grid = grid[h:batch_end]
            
            # Get pixel colors at grid positions
            pixels = np.array([img[y, x] for y, x in batch_grid])
            
            # Compute color probabilities for this batch
            color_probabilities = compute_color_probabilities(pixels, palette, k=color_randomness)
            
            # Draw strokes for this batch
            for i, (y, x) in enumerate(batch_grid):
                # Select color based on probability
                color = color_select(color_probabilities[i], palette)
                color_tuple = (int(color[0]), int(color[1]), int(color[2]))
                
                # Calculate stroke angle and length based on gradient
                angle = math.degrees(gradient.direction(y, x)) + 90
                length = int(round(stroke_scale + stroke_scale * math.sqrt(gradient.magnitude(y, x))))
                
                # Draw elliptical brush stroke
                cv2.ellipse(result, (x, y), (length, stroke_scale), angle, 0, 360, color_tuple, -1, cv2.LINE_AA)
        
        # Convert back to PIL Image (RGB)
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        return Image.fromarray(result_rgb)
        
    except Exception as e:
        raise Exception(f"Ronchetti algorithm failed: {str(e)}")

# Test the algorithm (optional)
if __name__ == "__main__":
    print("Testing Ronchetti algorithm...")
    
    try:
        # Load a test image
        with open("test_image.jpg", "rb") as f:
            image_data = f.read()
        
        # Test basic functionality
        result = create_pointillism(image_data)
        result.save("test_ronchetti_output.png")
        print("✅ Basic test completed!")
        
        # Test with custom parameters
        custom_params = {
            'palette_size': 15,
            'stroke_scale': 3,
            'gradient_smoothing': 2,
            'grid_scale': 4,
            'color_randomness': 7,
            'use_median_blur': True
        }
        
        result = create_pointillism(image_data, **custom_params)
        result.save("test_ronchetti_custom.png")
        print("✅ Custom parameters test completed!")
        
    except FileNotFoundError:
        print("⚠️  No test image found. Create a 'test_image.jpg' file to test the algorithm.")
    except Exception as e:
        print(f"❌ Test failed: {e}")
