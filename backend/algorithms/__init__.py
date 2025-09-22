"""
Algorithm Plugin System for Pointillism Generator
Automatically discovers and loads algorithms from Python files
"""

import os
import importlib
import inspect
from typing import Dict, List, Any

def discover_algorithms() -> Dict[str, Dict[str, Any]]:
    """
    Discover all algorithms in the algorithms folder
    
    Returns:
        Dict mapping algorithm keys to their metadata and functions
    """
    algorithms = {}
    algorithms_dir = os.path.dirname(__file__)
    
    # Get all Python files in the algorithms directory
    for filename in os.listdir(algorithms_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            algorithm_key = filename[:-3]  # Remove .py extension
            
            try:
                # Import the module
                module = importlib.import_module(f'algorithms.{algorithm_key}')
                
                # Check if it has the required function and is not hidden
                if hasattr(module, 'create_pointillism') and not getattr(module, 'ALGORITHM_HIDDEN', False):
                    # Extract metadata
                    metadata = {
                        'name': getattr(module, 'ALGORITHM_NAME', algorithm_key.title()),
                        'description': getattr(module, 'ALGORITHM_DESCRIPTION', 'No description available'),
                        'author': getattr(module, 'ALGORITHM_AUTHOR', 'Unknown'),
                        'version': getattr(module, 'ALGORITHM_VERSION', '1.0.0'),
                        'parameters': getattr(module, 'ALGORITHM_PARAMETERS', []),
                        'function': module.create_pointillism
                    }
                    
                    algorithms[algorithm_key] = metadata
                    print(f"Loaded algorithm: {metadata['name']} by {metadata['author']}")
                elif getattr(module, 'ALGORITHM_HIDDEN', False):
                    print(f"Skipping hidden algorithm: {algorithm_key}")
                    
            except Exception as e:
                print(f"Failed to load algorithm {algorithm_key}: {str(e)}")
                continue
    
    return algorithms

def get_algorithm_list() -> List[Dict[str, str]]:
    """
    Get list of available algorithms for frontend
    
    Returns:
        List of dictionaries with algorithm info
    """
    algorithms = discover_algorithms()
    return [
        {
            'key': key,
            'name': metadata['name'],
            'description': metadata['description'],
            'author': metadata['author'],
            'version': metadata['version'],
            'parameters': metadata['parameters']
        }
        for key, metadata in algorithms.items()
    ]

def get_algorithm_function(algorithm_key: str):
    """
    Get the algorithm function by key
    
    Args:
        algorithm_key: The key of the algorithm to get
        
    Returns:
        The algorithm function
        
    Raises:
        KeyError: If algorithm not found
    """
    algorithms = discover_algorithms()
    if algorithm_key not in algorithms:
        raise KeyError(f"Algorithm '{algorithm_key}' not found")
    
    return algorithms[algorithm_key]['function']
