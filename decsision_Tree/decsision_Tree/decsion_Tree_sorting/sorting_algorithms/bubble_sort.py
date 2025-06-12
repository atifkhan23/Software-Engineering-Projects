def bubble_sort(arr, track_comparisons=False):
    """
    Performs bubble sort on the provided list.
    
    If track_comparisons is True, returns the total number of comparisons made.
    Otherwise, sorts the list in-place and returns the sorted list.
    """
    comparisons = 0
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return comparisons if track_comparisons else arr
