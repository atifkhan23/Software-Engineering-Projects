from flask import Flask, render_template, request, jsonify
import numpy as np

# Import decision tree generator and analysis module.
from decision_tree.tree_generator import build_decision_tree
from analysis.average_case_analysis import run_analysis

app = Flask(__name__)

# Route to serve the front-end HTML
@app.route("/")
def home():
    return render_template("index.html")

# For demonstration, we implement a bubble sort that logs operations.
def bubble_sort_with_log(arr):
    operations_log = []
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            op_compare = {
                "type": "compare",
                "indices": (j, j + 1),
                "values": (arr[j], arr[j + 1]),
                "list_state": arr.copy()
            }
            operations_log.append(op_compare)
            if arr[j] > arr[j + 1]:
                op_swap = {
                    "type": "swap",
                    "indices": (j, j + 1),
                    "values": (arr[j], arr[j + 1]),
                    "list_state": arr.copy()
                }
                operations_log.append(op_swap)
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr, operations_log

def tree_to_dict(node):
    if node is None:
        return None
    return {
        "operation": node.operation,
        "state": node.state,
        "children": [tree_to_dict(child) for child in node.children]
    }

@app.route('/api/run_sort', methods=['POST'])
def run_sort():
    data = request.get_json()
    algorithm = data.get("algorithm", "bubble_sort")
    list_size = data.get("list_size", 10)
    
    if algorithm != "bubble_sort":
        return jsonify({"error": "Currently only bubble_sort is implemented with logging"}), 400
    
    arr = np.random.randint(1, 100, list_size).tolist()
    sorted_arr, operations_log = bubble_sort_with_log(arr.copy())
    decision_tree = None
    if list_size <= 4:
        tree_root = build_decision_tree(operations_log)
        decision_tree = tree_to_dict(tree_root)
    
    response = {
        "algorithm": algorithm,
        "original_array": arr,
        "sorted_array": sorted_arr,
        "comparisons": len([op for op in operations_log if op["type"] == "compare"]),
        "operations_log": operations_log if list_size <= 4 else "Log omitted for large input",
        "decision_tree": decision_tree if list_size <= 4 else "Decision tree not generated for large input"
    }
    return jsonify(response)

@app.route('/api/analysis', methods=['GET'])
def analysis():
    analysis_results = run_analysis()
    return jsonify(analysis_results)

if __name__ == "__main__":
    app.run(debug=True)
