def heap_sort(arr, track_comparisons=False):
    """
    Performs heap sort on the provided list.
    
    If track_comparisons is True, returns the total number of comparisons made.
    Otherwise, sorts the list in-place and returns the sorted list.
    """
    comparisons = 0

    def heapify(n, i):
        nonlocal comparisons
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n:
            comparisons += 1
            if arr[left] > arr[largest]:
                largest = left

        if right < n:
            comparisons += 1
            if arr[right] > arr[largest]:
                largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(n, largest)

    n = len(arr)
    # Build a max heap.
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    # Extract elements one by one.
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)

    return comparisons if track_comparisons else arr
