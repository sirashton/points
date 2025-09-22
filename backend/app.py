from flask import Flask, request, jsonify
from flask_cors import CORS
import io
from algorithms import discover_algorithms, get_algorithm_function

app = Flask(__name__)
CORS(app)

@app.route('/api/algorithms', methods=['GET'])
def get_algorithms():
    """
    Get list of available algorithms
    """
    try:
        from algorithms import get_algorithm_list
        algorithms = get_algorithm_list()
        return jsonify({
            'success': True,
            'algorithms': algorithms
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/process', methods=['POST'])
def process_image():
    """
    Process image using selected algorithm
    """
    try:
        # Get parameters
        dot_size = int(request.form.get('dot_size', 5))
        dot_count = int(request.form.get('dot_count', 1000))
        algorithm = request.form.get('algorithm', 'simple')
        
        # Get uploaded file
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        # Read image data
        image_data = file.read()
        
        # Get algorithm function
        try:
            algorithm_func = get_algorithm_function(algorithm)
        except KeyError:
            return jsonify({'error': f'Algorithm "{algorithm}" not found'}), 400
        
        # Get all parameters for the selected algorithm
        custom_params = {}
        for key, value in request.form.items():
            if key not in ['algorithm', 'image']:
                # Try to convert to appropriate type
                try:
                    # Check if it's a number
                    if '.' in value:
                        custom_params[key] = float(value)
                    else:
                        custom_params[key] = int(value)
                except ValueError:
                    # Keep as string
                    custom_params[key] = value
        
        # Process image using selected algorithm
        result_image = algorithm_func(image_data, **custom_params)
        
        # Convert to base64 for preview
        img_io = io.BytesIO()
        result_image.save(img_io, format='PNG')
        img_io.seek(0)
        
        import base64
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'image_data': f'data:image/png;base64,{img_base64}',
            'filename': f'pointillism_{algorithm}_result.png'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Discover and print available algorithms
    print("Discovering algorithms...")
    algorithms = discover_algorithms()
    for key, metadata in algorithms.items():
        print(f"  - {metadata['name']} by {metadata['author']} ({key})")
    
    app.run(debug=True, host='0.0.0.0', port=5000)