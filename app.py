from flask import Flask, request, jsonify
import time
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from factorial import bubble_sort, linear_search, binary_search, nested_loops
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, Text, MetaData, insert, select

app = Flask(__name__)

engine = create_engine("mysql+pymysql://root:spatni@localhost:3306/hbnb_db", echo=False)
metadata = MetaData()

analysis_results = Table(
    "analysis_results",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("algo", String(50)),
    Column("items", Integer),
    Column("steps", Integer),
    Column("start_time", Float),
    Column("end_time", Float),
    Column("total_time_ms", Float),
    Column("time_complexity", String(20)),
    Column("graph_base64", Text)
)

try:
    metadata.create_all(engine)
    DB_OK = True
except Exception as e:
    print(f"DB error: {e}")
    DB_OK = False

ALGOS = {
    "bubble": (bubble_sort, "Bubble Sort", "O(n²)"),
    "linear": (linear_search, "Linear Search", "O(n)"),
    "binary": (binary_search, "Binary Search", "O(log n)"),
    "nested": (nested_loops, "Nested Loops", "O(n²)")
}

@app.route("/")
def home():
    return jsonify({"available": list(ALGOS.keys()), "example": "/analyze?algo=bubble&n=1000&steps=10"})

@app.route("/analyze")
def analyze():
    algo = request.args.get("algo", "").strip('"\'').lower()
    n = request.args.get("n", type=int)
    steps = request.args.get("steps", type=int)

    if not algo or algo not in ALGOS:
        return jsonify({"error": "Invalid algo"}), 400
    if not n or n <= 0 or not steps or steps <= 0:
        return jsonify({"error": "Invalid n or steps"}), 400
    if steps > n:
        return jsonify({"error": "steps > n"}), 400

    algo_fn, name, complexity = ALGOS[algo]
    
    sizes = []
    times = []
    for size in range(steps, n + 1, steps):
        start = time.time()
        algo_fn(size)
        end = time.time()
        sizes.append(size)
        times.append(end - start)

    start_ms = int(time.time() * 1000)
    
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, marker="o", color="#2196F3", linewidth=2)
    plt.xlabel("Input Size")
    plt.ylabel("Time (s)")
    plt.title(f"{name} - {complexity}")
    plt.grid(True, alpha=0.5)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    graph_b64 = base64.b64encode(buf.read()).decode("utf-8")
    end_ms = int(time.time() * 1000)

    return jsonify({
        "algo": name,
        "items": n,
        "steps": steps,
        "start_time": start_ms,
        "end_time": end_ms,
        "total_time_ms": end_ms - start_ms,
        "time_complexity": complexity,
        "graph_base64": f"data:image/png;base64,{graph_b64}"
    })

@app.route("/save_analysis", methods=["POST"])
def save_analysis():
    if not DB_OK:
        return jsonify({"error": "DB not available"}), 503

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400

    required = ["algo", "items", "steps", "start_time", "end_time", "total_time_ms", "time_complexity"]
    if any(f not in data for f in required):
        return jsonify({"error": "Missing fields"}), 400

    stmt = insert(analysis_results).values(
        algo=data["algo"],
        items=data["items"],
        steps=data["steps"],
        start_time=data["start_time"],
        end_time=data["end_time"],
        total_time_ms=data["total_time_ms"],
        time_complexity=data["time_complexity"],
        graph_base64=data.get("graph_base64", "")
    )

    try:
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return jsonify({"status": "success", "id": result.inserted_primary_key[0]}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/retrieve_analysis")
def retrieve_analysis():
    if not DB_OK:
        return jsonify({"error": "DB not available"}), 503

    aid = request.args.get("id", type=int)
    if not aid:
        return jsonify({"error": "Missing id"}), 400

    stmt = select(analysis_results).where(analysis_results.c.id == aid)
    
    try:
        with engine.connect() as conn:
            result = conn.execute(stmt).fetchone()
            if not result:
                return jsonify({"error": "Not found"}), 404
            
            return jsonify({
                "id": result.id,
                "algo": result.algo,
                "items": result.items,
                "steps": result.steps,
                "start_time": result.start_time,
                "end_time": result.end_time,
                "total_time_ms": result.total_time_ms,
                "time_complexity": result.time_complexity,
                "graph_base64": result.graph_base64
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Running on http://localhost:3000")
    app.run(host="0.0.0.0", port=3000, debug=True)
