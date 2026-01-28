import time
import base64
import io
import os
import uuid
from datetime import datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Directory to save graphs
GRAPHS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphs')

# Create graphs directory if it doesn't exist
if not os.path.exists(GRAPHS_DIR):
    os.makedirs(GRAPHS_DIR)

# ==================== ALGORITHMS ====================

def linear_search(n):
    """Linear search - O(n) time complexity"""
    for i in range(n):
        if i == n - 1:
            return i

def bubble_sort(n):
    """Bubble sort - O(n²) time complexity"""
    arr = np.random.randint(0, 100, n)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def binary_search(n):
    """Binary search - O(log n) time complexity"""
    arr = sorted(np.random.randint(0, 100, n))
    target = arr[-1]
    left, right = 0, n - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def nested_loops(n):
    """Nested loops - O(n²) time complexity (exponential-like behavior)"""
    count = 0
    for i in range(n):
        for j in range(n):
            count += 1
    return count

# ==================== ALGORITHM MAPPING ====================

ALGORITHMS = {
    'bubble': {
        'func': bubble_sort,
        'name': 'Bubble Sort',
        'complexity': 'O(n²)'
    },
    'linear': {
        'func': linear_search,
        'name': 'Linear Search',
        'complexity': 'O(n)'
    },
    'binary': {
        'func': binary_search,
        'name': 'Binary Search',
        'complexity': 'O(log n)'
    },
    'nested': {
        'func': nested_loops,
        'name': 'Nested Loops',
        'complexity': 'O(n²)'
    }
}

# ==================== ANALYSIS FUNCTION ====================

def analyze_algorithm(algorithm_func, n_max, n_step):
    """
    Run the algorithm with increasing input sizes and measure execution times.
    Returns input sizes and corresponding execution times.
    """
    times = []
    input_sizes = list(range(n_step, n_max + n_step, n_step))
    
    for n in input_sizes:
        start = time.time()
        algorithm_func(n)
        end = time.time()
        times.append(end - start)
    
    return input_sizes, times

def generate_graph(input_sizes, times, algo_name, complexity, save_to_file=True):
    """
    Generate a graph of the algorithm's time complexity.
    Returns the graph as a base64 encoded string and optionally saves to file.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(input_sizes, times, 'o-', color='#2196F3', linewidth=2, markersize=4)
    ax.fill_between(input_sizes, times, alpha=0.3, color='#2196F3')
    
    ax.set_xlabel('Input Size (n)', fontsize=12)
    ax.set_ylabel('Running Time (seconds)', fontsize=12)
    ax.set_title(f'Time Complexity Analysis: {algo_name}\nTheoretical Complexity: {complexity}', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add stats annotation
    avg_time = np.mean(times)
    max_time = np.max(times)
    ax.annotate(f'Avg: {avg_time:.4f}s\nMax: {max_time:.4f}s', 
                xy=(0.02, 0.98), xycoords='axes fraction',
                verticalalignment='top',
                fontsize=10,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    # Save to bytes buffer for base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150)
    buffer.seek(0)
    
    # Save to file
    file_path = None
    if save_to_file:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f'{algo_name.lower().replace(" ", "_")}_{timestamp}_{unique_id}.png'
        file_path = os.path.join(GRAPHS_DIR, filename)
        plt.savefig(file_path, format='png', dpi=150)
    
    plt.close(fig)
    
    # Encode to base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64, file_path

# ==================== API ENDPOINTS ====================

@app.route('/')
def home():
    """Home endpoint with API information"""
    return jsonify({
           'available_algorithms': list(ALGORITHMS.keys()),
        'example': '/analyze?algo=bubble&n=1000&steps=10'
    })

@app.route('/analyze')
def analyze():
    """
    Main endpoint to analyze algorithm time complexity.
    
    Query Parameters:
    - algo: Algorithm to analyze (bubble, linear, binary, nested)
    - n: Maximum input size (number of elements)
    - steps: Step increment for input sizes
    """
    # Get query parameters
    algo = request.args.get('algo', '').strip().strip('"').strip("'").lower()
    n = request.args.get('n', type=int)
    steps = request.args.get('steps', type=int)
    
    # Validate parameters
    if not algo:
        return jsonify({'error': 'Missing required parameter: algo'}), 400
    
    if algo not in ALGORITHMS:
        return jsonify({
            'error': f'Unknown algorithm: {algo}',
            'available_algorithms': list(ALGORITHMS.keys())
        }), 400
    
    if not n or n <= 0:
        return jsonify({'error': 'Missing or invalid parameter: n (must be positive integer)'}), 400
    
    if not steps or steps <= 0:
        return jsonify({'error': 'Missing or invalid parameter: steps (must be positive integer)'}), 400
    
    if steps > n:
        return jsonify({'error': 'steps cannot be greater than n'}), 400
    
    # Get algorithm info
    algo_info = ALGORITHMS[algo]
    algorithm_func = algo_info['func']
    algo_name = algo_info['name']
    complexity = algo_info['complexity']
    
    # Record start time
    start_time = time.time()
    start_time_ms = int(start_time * 1000)
    
    # Run analysis
    input_sizes, times = analyze_algorithm(algorithm_func, n, steps)
    
    # Generate graph and save to file
    image_base64, file_path = generate_graph(input_sizes, times, algo_name, complexity, save_to_file=True)
    
    # Record end time
    end_time = time.time()
    end_time_ms = int(end_time * 1000)
    total_time_ms = end_time_ms - start_time_ms
    
    # Build response
    response = {
        'algo': algo_name,
        'items': str(n),
        'steps': str(steps),
        'start_time': start_time_ms,
        'end_time': end_time_ms,
        'total_time_ms': total_time_ms,
        'time_complexity': complexity,
        'data_points': len(input_sizes),
        'path_to_graph': file_path,
        'download_url': f'/download/{os.path.basename(file_path)}' if file_path else None,
        'graph_base64': f'data:image/png;base64,{image_base64}'
    }
    
    return jsonify(response)

@app.route('/download/<filename>')
def download_graph(filename):
    """Download a saved graph image"""
    file_path = os.path.join(GRAPHS_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=filename)
    return jsonify({'error': 'File not found'}), 404

@app.route('/graphs')
def list_graphs():
    """List all saved graphs"""
    if os.path.exists(GRAPHS_DIR):
        files = os.listdir(GRAPHS_DIR)
        graphs = [{'filename': f, 'download_url': f'/download/{f}'} for f in files if f.endswith('.png')]
        return jsonify({'graphs': graphs, 'total': len(graphs)})
    return jsonify({'graphs': [], 'total': 0})

@app.route('/algorithms')
def list_algorithms():
    """List all available algorithms"""
    algorithms = []
    for key, value in ALGORITHMS.items():
        algorithms.append({
            'key': key,
            'name': value['name'],
            'complexity': value['complexity']
        })
    return jsonify({'algorithms': algorithms})

# ==================== RUN SERVER ====================

if __name__ == '__main__':
    print("=" * 50)
    print("Algorithm Complexity Visualizer API")
    print("=" * 50)
    print("Server running at: http://localhost:3000")
    print("Example: http://localhost:3000/analyze?algo=bubble&n=1000&steps=10")
    print("=" * 50)
    app.run(host='0.0.0.0', port=3000, debug=True)
