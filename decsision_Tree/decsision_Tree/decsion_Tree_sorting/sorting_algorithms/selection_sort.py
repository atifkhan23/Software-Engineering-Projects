def selection_sort(arr, track_comparisons=False):
    """
    Performs selection sort on the provided list.
    
    If track_comparisons is True, returns the total number of comparisons made.
    Otherwise, sorts the list in-place and returns the sorted list.
    """
    comparisons = 0
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_index]:
                min_index = j
        if i != min_index:
            arr[i], arr[min_index] = arr[min_index], arr[i]
    return comparisons if track_comparisons else arr
