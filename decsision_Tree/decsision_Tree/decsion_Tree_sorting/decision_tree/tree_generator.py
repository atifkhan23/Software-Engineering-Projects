class TreeNode:
    def __init__(self, operation=None, state=None):
        """
        Represents a node in the decision tree.

        Parameters:
        - operation: dict containing details about the operation (e.g., type, indices, values).
        - state: the state of the list after this operation.
        """
        self.operation = operation  # A dictionary with operation details
        self.state = state          # List state at this node
        self.children = []          # List of child nodes

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        op_type = self.operation.get("type") if self.operation else "None"
        return f"TreeNode(op={op_type}, state={self.state}, children={len(self.children)})"


def build_decision_tree(operations_log, max_nodes=100):
    """
    Build a decision tree from a list of operation logs.
    Supports different sorting approaches by allowing branching based on unique states.
    To avoid an overly large tree for large inputs, only a sample of operations is used.
    
    Parameters:
    - operations_log: list of operation dictionaries.
    - max_nodes: maximum number of nodes to include in the tree.
    
    Each log entry should be a dictionary with keys:
      - 'type': type of operation (e.g., "compare", "swap", "shift", "merge", "insert")
      - 'indices': tuple of indices involved
      - 'values': the values involved in the operation
      - 'list_state': state of the list after the operation

    Returns the root node of the decision tree.
    """
    if not operations_log:
        return None

    total_ops = len(operations_log)
    # Determine sample rate; use every operation if total_ops <= max_nodes
    sample_rate = 1 if total_ops <= max_nodes else total_ops // max_nodes

    # Create the root node from the first operation
    root = TreeNode(operation=operations_log[0], state=operations_log[0].get("list_state"))
    nodes = {tuple(root.state): root}  # Track unique states

    # Build tree by sampling the operations log
    for i in range(1, total_ops):
        if i % sample_rate != 0:
            continue
        op = operations_log[i]
        state_tuple = tuple(op.get("list_state"))
        new_node = TreeNode(operation=op, state=op.get("list_state"))
        # Link to the node whose state matches the previous operation's state
        prev_state_tuple = tuple(operations_log[i - 1].get("list_state"))
        parent_node = nodes.get(prev_state_tuple, root)
        parent_node.add_child(new_node)
        nodes[state_tuple] = new_node

    return root


def print_tree(node, level=0):
    """
    Recursively prints the decision tree structure for debugging/visualization.
    """
    if node is None:
        return
    indent = "  " * level
    op_type = node.operation.get("type") if node.operation else "None"
    print(f"{indent}Node: {op_type} | State: {node.state}")
    for child in node.children:
        print_tree(child, level + 1)


def get_subtree(root, start_index):
    """
    Retrieve a subtree starting from a given index in the decision tree.
    For a chain of operations, this returns the node after following the first child
    'start_index' times.
    """
    current = root
    for _ in range(start_index):
        if current and current.children:
            current = current.children[0]
        else:
            break
    return current


# ---- Sorting algorithms with logging ----

def bubble_sort_with_log(arr):
    log = []
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            # Log comparison
            log.append({
                "type": "compare",
                "indices": (j, j + 1),
                "values": (a[j], a[j + 1]),
                "list_state": list(a)
            })
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                log.append({
                    "type": "swap",
                    "indices": (j, j + 1),
                    "values": (a[j], a[j + 1]),
                    "list_state": list(a)
                })
    return a, log


def insertion_sort_with_log(arr):
    log = []
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            log.append({
                "type": "compare",
                "indices": (j, i),
                "values": (a[j], key),
                "list_state": list(a)
            })
            # Shift the element to the right
            a[j + 1] = a[j]
            log.append({
                "type": "shift",
                "indices": (j, j + 1),
                "values": (a[j], key),
                "list_state": list(a)
            })
            j -= 1
        a[j + 1] = key
        log.append({
            "type": "insert",
            "indices": (j + 1,),
            "values": (key,),
            "list_state": list(a)
        })
    return a, log


def heap_sort_with_log(arr):
    log = []
    a = arr.copy()
    n = len(a)

    def heapify(a, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n:
            log.append({
                "type": "compare",
                "indices": (i, l),
                "values": (a[largest], a[l]),
                "list_state": list(a)
            })
            if a[l] > a[largest]:
                largest = l

        if r < n:
            log.append({
                "type": "compare",
                "indices": (largest, r),
                "values": (a[largest], a[r]),
                "list_state": list(a)
            })
            if a[r] > a[largest]:
                largest = r

        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            log.append({
                "type": "swap",
                "indices": (i, largest),
                "values": (a[i], a[largest]),
                "list_state": list(a)
            })
            heapify(a, n, largest)

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(a, n, i)

    # Heap sort
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        log.append({
            "type": "swap",
            "indices": (0, i),
            "values": (a[0], a[i]),
            "list_state": list(a)
        })
        heapify(a, i, 0)

    return a, log


def merge_sort_with_log(arr):
    log = []
    a = arr.copy()

    def merge_sort_recursive(a, left, right):
        if right - left > 1:
            mid = (left + right) // 2
            merge_sort_recursive(a, left, mid)
            merge_sort_recursive(a, mid, right)
            merge(a, left, mid, right)

    def merge(a, left, mid, right):
        left_part = a[left:mid]
        right_part = a[mid:right]
        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            log.append({
                "type": "compare",
                "indices": (left + i, mid + j),
                "values": (left_part[i], right_part[j]),
                "list_state": list(a)
            })
            if left_part[i] <= right_part[j]:
                a[k] = left_part[i]
                i += 1
            else:
                a[k] = right_part[j]
                j += 1
            log.append({
                "type": "merge",
                "indices": (k,),
                "values": (a[k],),
                "list_state": list(a)
            })
            k += 1
        while i < len(left_part):
            a[k] = left_part[i]
            log.append({
                "type": "merge",
                "indices": (k,),
                "values": (a[k],),
                "list_state": list(a)
            })
            i += 1
            k += 1
        while j < len(right_part):
            a[k] = right_part[j]
            log.append({
                "type": "merge",
                "indices": (k,),
                "values": (a[k],),
                "list_state": list(a)
            })
            j += 1
            k += 1

    merge_sort_recursive(a, 0, len(a))
    return a, log


def quick_sort_with_log(arr):
    log = []
    a = arr.copy()

    def quick_sort_recursive(a, low, high):
        if low < high:
            pivot_index = partition(a, low, high)
            quick_sort_recursive(a, low, pivot_index - 1)
            quick_sort_recursive(a, pivot_index + 1, high)

    def partition(a, low, high):
        pivot = a[high]  # Choose the last element as pivot
        i = low - 1
        for j in range(low, high):
            log.append({
                "type": "compare",
                "indices": (j, high),
                "values": (a[j], pivot),
                "list_state": list(a)
            })
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
                log.append({
                    "type": "swap",
                    "indices": (i, j),
                    "values": (a[i], a[j]),
                    "list_state": list(a)
                })
        a[i + 1], a[high] = a[high], a[i + 1]
        log.append({
            "type": "swap",
            "indices": (i + 1, high),
            "values": (a[i + 1], a[high]),
            "list_state": list(a)
        })
        return i + 1

    quick_sort_recursive(a, 0, len(a) - 1)
    return a, log


def selection_sort_with_log(arr):
    log = []
    a = arr.copy()
    n = len(a)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            log.append({
                "type": "compare",
                "indices": (min_index, j),
                "values": (a[min_index], a[j]),
                "list_state": list(a)
            })
            if a[j] < a[min_index]:
                min_index = j
        if min_index != i:
            a[i], a[min_index] = a[min_index], a[i]
            log.append({
                "type": "swap",
                "indices": (i, min_index),
                "values": (a[i], a[min_index]),
                "list_state": list(a)
            })
    return a, log


# ---- Main execution: take user input, run each sort, and generate its decision tree ----

if __name__ == "__main__":
    user_input = input("Enter a list of numbers separated by spaces: ")
    try:
        test_list = list(map(int, user_input.strip().split()))
    except ValueError:
        print("Invalid input. Please enter only numbers separated by spaces.")
        exit(1)

    algorithms = {
        "Bubble Sort": bubble_sort_with_log,
        "Insertion Sort": insertion_sort_with_log,
        "Heap Sort": heap_sort_with_log,
        "Merge Sort": merge_sort_with_log,
        "Quick Sort": quick_sort_with_log,
        "Selection Sort": selection_sort_with_log
    }
    
    for name, sort_func in algorithms.items():
        print(f"\n{name}:")
        sorted_list, op_log = sort_func(test_list)
        print(f"Sorted list: {sorted_list}")
        # Use our adjusted decision tree builder with sampling
        tree = build_decision_tree(op_log, max_nodes=100)
        print("Decision Tree:")
        print_tree(tree)
