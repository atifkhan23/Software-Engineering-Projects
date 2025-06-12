def insertion_sort(arr, track_comparisons=False):
    """
    Performs insertion sort on the provided list.
    
    If track_comparisons is True, returns the total number of comparisons made.
    Otherwise, sorts the list in-place and returns the sorted list.
    """
    comparisons = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = key
    return comparisons if track_comparisons else arr
