def quick_sort(arr, track_comparisons=False):
    """
    Performs quick sort on the provided list.
    
    If track_comparisons is True, returns the total number of comparisons made.
    Otherwise, sorts the list in-place and returns the sorted list.
    """
    comparisons = 0

    def _quick_sort(lst, low, high):
        nonlocal comparisons
        if low < high:
            pivot_index = partition(lst, low, high)
            _quick_sort(lst, low, pivot_index - 1)
            _quick_sort(lst, pivot_index + 1, high)

    def partition(lst, low, high):
        nonlocal comparisons
        pivot = lst[high]
        i = low - 1
        for j in range(low, high):
            comparisons += 1
            if lst[j] <= pivot:
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        return i + 1

    _quick_sort(arr, 0, len(arr) - 1)
    return comparisons if track_comparisons else arr
