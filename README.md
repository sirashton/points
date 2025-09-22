# Pointillism Generator

A web application that converts uploaded images into beautiful pointillism art using various algorithms. Features a plugin architecture that allows developers to easily add new algorithms with custom parameters.

## 🎨 Features

- **Multiple Algorithms**: 6 built-in pointillism algorithms
- **Dynamic UI**: Custom parameters automatically generate UI controls
- **Plugin System**: Easy to add new algorithms
- **Real-time Processing**: Generate art with custom settings
- **Docker Support**: Easy deployment and development
- **Responsive Design**: Works on desktop and mobile

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Modern web browser

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

## 🎯 Available Algorithms

| Algorithm | Description | Custom Parameters |
|-----------|-------------|-------------------|
| **Simple Dots** | Basic uniform circular dots | None |
| **Enhanced Dots** | Smart color palette with limited size variation | None |
| **Original Strokes** | Brush strokes with adaptive density | None |
| **Ronchetti Original** | Matteo Ronchetti's adaptive approach | None |
| **Watercolor** | Soft, flowing watercolor effects | 4 parameters |
| **Impressionist** | Impressionist styles with artistic controls | 5 parameters |

## 🛠️ For Developers

### Adding New Algorithms

1. **Copy the template**:
   ```bash
   cp backend/algorithms/template.py backend/algorithms/my_algorithm.py
   ```

2. **Customize your algorithm**:
   - Update metadata (name, description, author)
   - Implement your pointillism logic
   - Add custom parameters if needed

3. **Restart the application**:
   ```bash
   docker-compose restart
   ```

### Documentation

- **Getting Started**: `GETTING_STARTED.md` - Quick start guide
- **Developer Guide**: `DEVELOPER_GUIDE.md` - Comprehensive development guide
- **Algorithm README**: `backend/algorithms/README.md` - Algorithm development reference
- **Template**: `backend/algorithms/template.py` - Algorithm template

### Example Algorithm

```python
# Required metadata
ALGORITHM_NAME = "My Algorithm"
ALGORITHM_DESCRIPTION = "Creates beautiful pointillism art"
ALGORITHM_AUTHOR = "Your Name"
ALGORITHM_VERSION = "1.0.0"

# Optional custom parameters
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
    }
]

def create_pointillism(image_data, dot_size, dot_count, **custom_params):
    # Your algorithm implementation
    return PIL.Image
```

## 🏗️ Architecture

### Frontend
- **React + Vite**: Modern web framework
- **Dynamic UI**: Automatically generates controls from algorithm parameters
- **Real-time Updates**: Immediate parameter changes

### Backend
- **Flask**: Python web framework
- **Plugin System**: Dynamic algorithm discovery and loading
- **Image Processing**: PIL/OpenCV for image manipulation

### Containerization
- **Docker**: Containerized deployment
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Frontend serving and API proxying

## 📁 Project Structure

```
points/
├── backend/
│   ├── algorithms/           # Algorithm plugins
│   │   ├── template.py      # Algorithm template
│   │   ├── simple.py        # Basic algorithm
│   │   ├── watercolor.py    # Example with parameters
│   │   └── README.md        # Algorithm documentation
│   ├── app.py               # Flask backend
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   └── index.css        # Styles
│   └── package.json         # Node dependencies
├── docker-compose.yml       # Container orchestration
├── GETTING_STARTED.md       # Quick start guide
├── DEVELOPER_GUIDE.md       # Development guide
└── README.md                # This file
```

## 🎨 How to Use

1. **Upload an Image**: Drag and drop or click to select
2. **Choose Algorithm**: Select from the dropdown menu
3. **Adjust Settings**: Use sliders and controls to customize
4. **Generate Art**: Click "Generate Pointillism Art"
5. **Download Result**: Save your pointillism artwork

## 🔧 Development

### Running in Development Mode

```bash
# Start with auto-reload
docker-compose up --build

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Adding Dependencies

**Backend (Python)**:
```bash
# Add to requirements.txt
echo "new-package==1.0.0" >> backend/requirements.txt
docker-compose up --build
```

**Frontend (Node.js)**:
```bash
# Add to package.json
npm install new-package
docker-compose up --build
```

## 🐛 Troubleshooting

### Common Issues

| **Issue** | **Solution** |
|-----------|--------------|
| Application won't start | Check Docker is running and ports 3000/5000 are free |
| Algorithm not appearing | Verify file is in `backend/algorithms/` with correct metadata |
| Parameters not working | Check `ALGORITHM_PARAMETERS` format is correct |
| Processing errors | Check `docker-compose logs backend` for error messages |

### Debugging

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Access backend container
docker-compose exec backend bash
```

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

## 📚 Resources

- **Algorithm Template**: `backend/algorithms/template.py`
- **Getting Started**: `GETTING_STARTED.md`
- **Developer Guide**: `DEVELOPER_GUIDE.md`
- **Algorithm Reference**: `backend/algorithms/README.md`

## 🎉 Success Stories

The plugin system has been used to create:

- **Watercolor Effects**: Soft, flowing pointillism with custom blur and palette controls
- **Impressionist Styles**: Multiple artistic styles with brush variation and color vibrancy
- **Adaptive Algorithms**: Smart algorithms that adjust to image complexity
- **Custom Parameters**: Rich UI controls for fine-tuning artistic output

## 🆘 Support

If you need help:

1. **Check the logs**: `docker-compose logs backend`
2. **Review examples**: Look at existing algorithm files
3. **Read documentation**: Check the guide files
4. **Ask questions**: Contact the project maintainers

## 🎨 License

This project is open source and available under the MIT License.

---

**Ready to create beautiful pointillism art?** Start with the [Getting Started Guide](GETTING_STARTED.md) or dive into the [Developer Guide](DEVELOPER_GUIDE.md) to add your own algorithms! 🎨✨