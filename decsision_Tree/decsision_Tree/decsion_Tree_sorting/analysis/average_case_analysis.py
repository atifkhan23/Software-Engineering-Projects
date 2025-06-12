import numpy as np
from sorting_algorithms.bubble_sort import bubble_sort
from sorting_algorithms.insertion_sort import insertion_sort
from sorting_algorithms.selection_sort import selection_sort
from sorting_algorithms.merge_sort import merge_sort
from sorting_algorithms.quick_sort import quick_sort
from sorting_algorithms.heap_sort import heap_sort

def yao_lower_bound(n):
    """Compute Yao's lower bound for sorting: Ω(n log n)"""
    return n * np.log2(n) if n > 1 else 0

def analyze_algorithm(sort_func, n, iterations=100):
    """
    Run a specified sorting function multiple times on random arrays of size n.
    Returns the average number of comparisons over the given iterations.
    """
    counts = []
    for _ in range(iterations):
        arr = np.random.randint(1, 100, n).tolist()
        comp = sort_func(arr, track_comparisons=True)
        counts.append(comp)
    return np.mean(counts)

def run_analysis():
    """
    Runs average-case analysis for each sorting algorithm on multiple input sizes.
    Returns a dictionary containing:
      - Average comparisons per algorithm.
      - Yao's lower bound for each test size.
      - Ratio of average comparisons to Yao's bound.
      - Simulated examples of decision tree configurations.
    """
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "Heap Sort": heap_sort
    }
    
    test_sizes = [10, 20, 50, 100]
    analysis_results = {}
    
    for n in test_sizes:
        algo_results = {}
        yao = yao_lower_bound(n)
        for name, func in algorithms.items():
            avg_comps = analyze_algorithm(func, n)
            algo_results[name] = {
                "average_comparisons": avg_comps,
                "yao_lower_bound": yao,
                "ratio_to_yao": avg_comps / yao if yao != 0 else None
            }
        analysis_results[n] = algo_results
    
    # Simulated examples of decision tree configurations.
    # These are dummy data to illustrate balanced, mixed, and imbalanced trees.
    tree_configurations = {
        "balanced_trees": {
            "description": "Example of two balanced decision trees.",
            "average_depth": 4,
            "max_depth": 5
        },
        "mixed_trees": {
            "description": "Example of one balanced and one imbalanced decision tree.",
            "balanced_tree": {"average_depth": 4, "max_depth": 5},
            "imbalanced_tree": {"average_depth": 8, "max_depth": 12}
        },
        "imbalanced_trees": {
            "description": "Example of two imbalanced decision trees.",
            "average_depth": 10,
            "max_depth": 15
        }
    }
    
    return {
        "analysis_results": analysis_results,
        "tree_configurations": tree_configurations
    }

if __name__ == "__main__":
    results = run_analysis()
    import json
    print(json.dumps(results, indent=2))
