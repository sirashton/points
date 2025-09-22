# Pointillism Generator - Developer Guide

Welcome to the Pointillism Generator project! This guide will help you understand the system architecture and how to contribute new algorithms.

## 🏗️ System Architecture

### Overview
The Pointillism Generator is a web application that converts uploaded images into pointillism art using various algorithms. It features a plugin architecture that allows developers to easily add new algorithms.

### Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Algorithms    │
│   (React/Vite)  │◄──►│   (Flask)       │◄──►│   (Python)      │
│                 │    │                 │    │                 │
│ • File Upload   │    │ • API Endpoints │    │ • Plugin System │
│ • Dynamic UI    │    │ • Image Process │    │ • Auto-Discovery│
│ • Real-time     │    │ • Parameter     │    │ • Custom Params │
│   Controls      │    │   Handling      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

- **Frontend**: React + Vite + CSS
- **Backend**: Python + Flask + PIL/OpenCV
- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (for frontend serving and API proxying)

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Basic Python knowledge
- Understanding of image processing concepts

### Running the Application

```bash
# Clone the repository
git clone <repository-url>
cd points

# Start the application
docker-compose up --build

# Access the application
open http://localhost:3000
```

## 🎨 Algorithm Development

### Quick Start

1. **Copy the template**:
   ```bash
   cp backend/algorithms/template.py backend/algorithms/my_algorithm.py
   ```

2. **Customize your algorithm**:
   - Update metadata (name, description, author)
   - Implement your pointillism logic
   - Add custom parameters if needed

3. **Test your algorithm**:
   ```bash
   cd backend/algorithms
   python my_algorithm.py
   ```

4. **Restart the application**:
   ```bash
   docker-compose restart
   ```

### Algorithm Structure

Every algorithm must have:

```python
# Required metadata
ALGORITHM_NAME = "Your Algorithm Name"
ALGORITHM_DESCRIPTION = "Brief description"
ALGORITHM_AUTHOR = "Your Name"
ALGORITHM_VERSION = "1.0.0"

# Optional custom parameters
ALGORITHM_PARAMETERS = [...]

# Required function
def create_pointillism(image_data, dot_size, dot_count, **custom_params):
    # Your algorithm implementation
    return PIL.Image
```

### Parameter Types

The system supports three types of UI controls:

#### 1. Slider (Numeric Range)
```python
{
    "name": "intensity",
    "type": "slider",
    "label": "Color Intensity",
    "min": 0.5,
    "max": 2.0,
    "step": 0.1,
    "default": 1.2,
    "description": "How intense the colors should be"
}
```

#### 2. Select (Dropdown)
```python
{
    "name": "style",
    "type": "select",
    "label": "Artistic Style",
    "options": [
        {"value": "soft", "label": "Soft & Gentle"},
        {"value": "bold", "label": "Bold & Expressive"}
    ],
    "default": "soft",
    "description": "Choose the artistic style"
}
```

#### 3. Checkbox (Boolean)
```python
{
    "name": "use_effect",
    "type": "checkbox",
    "label": "Apply Special Effect",
    "default": True,
    "description": "Add a special effect to the result"
}
```

## 🔧 Development Workflow

### 1. Algorithm Development

```bash
# Create your algorithm file
cp backend/algorithms/template.py backend/algorithms/my_algorithm.py

# Edit your algorithm
nano backend/algorithms/my_algorithm.py

# Test locally (optional)
python backend/algorithms/my_algorithm.py
```

### 2. Testing

```bash
# Test the full application
docker-compose up --build

# Check logs
docker-compose logs backend

# Test specific algorithm
# Upload an image and select your algorithm in the UI
```

### 3. Debugging

```bash
# View backend logs
docker-compose logs -f backend

# View frontend logs
docker-compose logs -f frontend

# Access backend container
docker-compose exec backend bash
```

## 📁 File Structure

```
points/
├── backend/
│   ├── algorithms/           # Algorithm plugins
│   │   ├── __init__.py      # Plugin system
│   │   ├── template.py      # Algorithm template
│   │   ├── simple.py        # Basic algorithm
│   │   ├── watercolor.py    # Example with parameters
│   │   └── README.md        # Algorithm documentation
│   ├── app.py               # Flask backend
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   └── index.css        # Styles
│   ├── package.json         # Node dependencies
│   └── Dockerfile           # Frontend container
├── docker-compose.yml       # Container orchestration
└── DEVELOPER_GUIDE.md       # This file
```

## 🎯 Best Practices

### Algorithm Design

1. **Performance**: Keep processing time under 30 seconds
2. **Quality**: Ensure consistent output across different images
3. **Error Handling**: Always handle exceptions gracefully
4. **Compatibility**: Return PIL.Image objects with correct dimensions

### Parameter Design

1. **Descriptive Names**: Use clear, descriptive parameter names
2. **Helpful Labels**: Provide user-friendly labels and descriptions
3. **Reasonable Ranges**: Choose appropriate min/max values for sliders
4. **Meaningful Options**: Use descriptive option labels for selects

### Code Quality

1. **Documentation**: Comment your code thoroughly
2. **Error Messages**: Provide meaningful error messages
3. **Testing**: Test with various image types and sizes
4. **Consistency**: Follow the existing code style

## 🐛 Troubleshooting

### Common Issues

| **Issue** | **Cause** | **Solution** |
|-----------|-----------|--------------|
| Algorithm not appearing | Missing metadata or function | Check required variables exist |
| Parameter controls not showing | Incorrect parameter format | Verify ALGORITHM_PARAMETERS format |
| Import errors | Missing dependencies | Check imports are available |
| Processing errors | Function doesn't return PIL.Image | Ensure correct return type |
| UI not updating | Frontend not reloaded | Restart docker-compose |

### Debugging Steps

1. **Check logs**: `docker-compose logs backend`
2. **Verify file location**: Ensure file is in `backend/algorithms/`
3. **Test syntax**: Run `python your_algorithm.py`
4. **Check metadata**: Verify all required variables exist
5. **Test parameters**: Ensure parameter format is correct

## 📚 Examples

### Basic Algorithm
See `backend/algorithms/simple.py` for a basic algorithm without custom parameters.

### Advanced Algorithm
See `backend/algorithms/watercolor.py` for an algorithm with custom parameters.

### Complex Algorithm
See `backend/algorithms/impressionist.py` for a complex algorithm with multiple parameter types.

## 🤝 Contributing

### Submitting Algorithms

1. **Create your algorithm** following the template
2. **Test thoroughly** with different images
3. **Document your approach** in comments
4. **Submit via pull request** or direct file submission

### Code Review Process

1. **Functionality**: Algorithm works correctly
2. **Performance**: Reasonable processing time
3. **Quality**: Consistent, high-quality output
4. **Documentation**: Clear comments and metadata
5. **Parameters**: Well-designed UI controls

## 📖 Additional Resources

- **Algorithm README**: `backend/algorithms/README.md`
- **Template File**: `backend/algorithms/template.py`
- **Example Algorithms**: Check existing algorithm files
- **Docker Documentation**: [Docker Compose Docs](https://docs.docker.com/compose/)

## 🆘 Support

If you need help:

1. **Check the logs**: `docker-compose logs backend`
2. **Review examples**: Look at existing algorithm files
3. **Test incrementally**: Start with basic functionality
4. **Ask questions**: Contact the project maintainers

## 🎉 Success!

Once your algorithm is working:

1. **Test with various images** to ensure robustness
2. **Verify UI controls** work as expected
3. **Check performance** with different image sizes
4. **Document your approach** for future reference

Your algorithm will be automatically integrated into the web application and available to all users! 🎨✨
