# Algorithm Complexity Visualizer

A Flask-based API that analyzes and visualizes the time complexity of various algorithms. Run different algorithms with varying input sizes and get detailed performance analysis with visual graphs.

## Features

- Real-time algorithm performance analysis
- Automatic graph generation with matplotlib
- Multiple algorithms: Bubble Sort, Linear Search, Binary Search, Nested Loops
- Base64 encoded graph images in JSON response
- Automatic graph saving to disk
- Download saved graphs via API
- Execution time tracking and statistics

## Installation

### Prerequisites

- Python 3.14+
- pip
- Tkinter support (for matplotlib)

### Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd complexity_visualizer
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install flask numpy matplotlib
   ```

4. **Install Tkinter** (macOS with Homebrew)
   ```bash
   brew install python-tk@3.14
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The server will start at: `http://localhost:3000`

## Available Algorithms

| Algorithm | Key | Time Complexity |
|-----------|-----|-----------------|
| Bubble Sort | `bubble` | O(n²) |
| Linear Search | `linear` | O(n) |
| Binary Search | `binary` | O(log n) |
| Nested Loops | `nested` | O(n²) |

## API Endpoints

### 1. Home - API Information
```
GET /
```
Returns available algorithms and example usage.

**Example:**
```bash
curl http://localhost:3000/
```

---

### 2. Analyze Algorithm
```
GET /analyze?algo=<algorithm>&n=<size>&steps=<step>
```

**Query Parameters:**
- `algo` (required): Algorithm to analyze (`bubble`, `linear`, `binary`, `nested`)
- `n` (required): Maximum input size (positive integer)
- `steps` (required): Step increment for input sizes (positive integer, must be ≤ n)

**Example:**
```bash
curl "http://localhost:3000/analyze?algo=bubble&n=1000&steps=10"
```

**Response:**
```json
{
  "algo": "Bubble Sort",
  "items": "1000",
  "steps": "10",
  "start_time": 1738108234567,
  "end_time": 1738108235892,
  "total_time_ms": 1325,
  "time_complexity": "O(n²)",
  "data_points": 100,
  "path_to_graph": "/path/to/graphs/bubble_sort_20260128_143715_a1b2c3d4.png",
  "download_url": "/download/bubble_sort_20260128_143715_a1b2c3d4.png",
  "graph_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```

---

### 3. List All Algorithms
```
GET /algorithms
```
Returns detailed information about all available algorithms.

**Example:**
```bash
curl http://localhost:3000/algorithms
```

---

### 4. List Saved Graphs
```
GET /graphs
```
Returns a list of all saved graph images with download URLs.

**Example:**
```bash
curl http://localhost:3000/graphs
```

---

### 5. Download Graph
```
GET /download/<filename>
```
Download a specific saved graph image.

**Example:**
```bash
curl -O http://localhost:3000/download/bubble_sort_20260128_143715_a1b2c3d4.png
```

## Usage Examples

**Analyze Bubble Sort:**
```bash
curl "http://localhost:3000/analyze?algo=bubble&n=1000&steps=10"
```

**Analyze Linear Search:**
```bash
curl "http://localhost:3000/analyze?algo=linear&n=5000&steps=100"
```

**Analyze Binary Search:**
```bash
curl "http://localhost:3000/analyze?algo=binary&n=10000&steps=500"
```

**Analyze Nested Loops:**
```bash
curl "http://localhost:3000/analyze?algo=nested&n=500&steps=10"
```

### Compare Algorithms
```bash
# Linear Search - O(n)
curl "http://localhost:3000/analyze?algo=linear&n=5000&steps=50"

# Binary Search - O(log n)
curl "http://localhost:3000/analyze?algo=binary&n=5000&steps=50"
```

## Project Structure

```
complexity_visualizer/
├── app.py                 # Main Flask application
├── README.md             # This file
├── factorial.py          # Factorial implementation
├── graphs/               # Auto-generated graph images
│   └── *.png
├── home_activity.txt     # Project requirements
├── class_activity.txt    # Class notes
└── .venv/                # Virtual environment (not tracked)
```

## Graph Features

Each generated graph includes:
- Line plot with markers showing execution time vs input size
- Shaded area under the curve for visual emphasis
- Grid for easier reading
- Title with algorithm name and theoretical complexity
- Statistics annotation (average and maximum execution times)
- Automatically saved with timestamp and unique ID

## Response Format

All `/analyze` responses include:
- **algo**: Algorithm name
- **items**: Maximum input size (n)
- **steps**: Step increment
- **start_time**: Analysis start timestamp (milliseconds)
- **end_time**: Analysis end timestamp (milliseconds)
- **total_time_ms**: Total execution time in milliseconds
- **time_complexity**: Theoretical Big O notation
- **data_points**: Number of measurements taken
- **path_to_graph**: Local file path to saved graph
- **download_url**: API endpoint to download the graph
- **graph_base64**: Base64 encoded PNG image with data URI prefix

## Error Handling

The API returns appropriate error messages for:
- Missing required parameters
- Invalid algorithm names
- Invalid input sizes or steps
- Step values greater than n
- File not found errors

## Development

### Run in Debug Mode
```bash
python app.py
```
Debug mode is enabled by default.

### Modify Port
Edit the last line in `app.py`:
```python
app.run(host='0.0.0.0', port=3000, debug=True)  # Change port here
```

## Notes

- Graphs are automatically saved to the `graphs/` directory
- Each graph filename includes a timestamp and unique identifier
- The API uses a non-interactive matplotlib backend (`Agg`) for server compatibility
- All execution times are measured in seconds
- Response times include both algorithm analysis and graph generation
- The `algo` parameter accepts values with or without quotes

## Requirements

- Flask 3.1.2+
- NumPy 2.4.1+
- Matplotlib (with Tkinter backend support)
- Python 3.14+

## License

Educational project for learning algorithm complexity analysis.

## Author

Created for school complexity visualization activities.
