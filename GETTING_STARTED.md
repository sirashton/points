# Getting Started - Pointillism Generator

Welcome! This guide will help you quickly add your own pointillism algorithm to the web application.

## 🚀 Quick Start (5 minutes)

### Step 1: Copy the Template
```bash
cp backend/algorithms/template.py backend/algorithms/my_algorithm.py
```

### Step 2: Edit Your Algorithm
Open `backend/algorithms/my_algorithm.py` and customize:

```python
# Change these
ALGORITHM_NAME = "My Awesome Algorithm"
ALGORITHM_DESCRIPTION = "Creates beautiful pointillism art"
ALGORITHM_AUTHOR = "Your Name"
ALGORITHM_VERSION = "1.0.0"

# Add your algorithm logic in the create_pointillism function
def create_pointillism(image_data, dot_size, dot_count, **custom_params):
    # Your code here
    pass
```

### Step 3: Test Your Algorithm
```bash
# Test locally (optional)
python backend/algorithms/my_algorithm.py

# Start the application
docker-compose up --build
```

### Step 4: Use Your Algorithm
1. Open http://localhost:3000
2. Upload an image
3. Select "My Awesome Algorithm" from the dropdown
4. Click "Generate Pointillism Art"

That's it! Your algorithm is now integrated into the web application.

## 🎨 Adding Custom Parameters

Want to add sliders, dropdowns, or checkboxes? Add this to your algorithm:

```python
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
        "label": "Art Style",
        "options": [
            {"value": "soft", "label": "Soft & Gentle"},
            {"value": "bold", "label": "Bold & Expressive"}
        ],
        "default": "soft",
        "description": "Choose the artistic style"
    },
    {
        "name": "use_blur",
        "type": "checkbox",
        "label": "Apply Blur",
        "default": True,
        "description": "Add a blur effect"
    }
]
```

Then use them in your function:
```python
def create_pointillism(image_data, dot_size, dot_count, **custom_params):
    intensity = custom_params.get('intensity', 1.2)
    style = custom_params.get('style', 'soft')
    use_blur = custom_params.get('use_blur', True)
    
    # Use these parameters in your algorithm
    # ...
```

## 📚 Examples

- **Basic**: `backend/algorithms/simple.py` - No custom parameters
- **Advanced**: `backend/algorithms/watercolor.py` - 4 custom parameters
- **Complex**: `backend/algorithms/impressionist.py` - 5 custom parameters

## 🐛 Troubleshooting

**Algorithm not appearing?**
- Check file is in `backend/algorithms/` directory
- Verify all required metadata variables exist
- Check `docker-compose logs backend` for errors

**Parameters not working?**
- Verify `ALGORITHM_PARAMETERS` format is correct
- Check parameter names match in function signature
- Restart the application after changes

**Need help?**
- Check `backend/algorithms/README.md` for detailed documentation
- Look at existing algorithm files for examples
- Review `DEVELOPER_GUIDE.md` for advanced topics

## 🎯 What's Next?

1. **Test your algorithm** with different images
2. **Add more parameters** to customize the experience
3. **Optimize performance** for better user experience
4. **Share your algorithm** with the community

Happy coding! 🎨✨
