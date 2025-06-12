def merge_sort(arr, track_comparisons=False):
    """
    Performs merge sort on the provided list.
    
    If track_comparisons is True, returns the total number of comparisons made.
    Otherwise, sorts the list (via returning a new sorted list) and returns it.
    """
    comparisons = 0

    def merge(left, right):
        nonlocal comparisons
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    def merge_sort_recursive(lst):
        if len(lst) <= 1:
            return lst
        mid = len(lst) // 2
        left = merge_sort_recursive(lst[:mid])
        right = merge_sort_recursive(lst[mid:])
        return merge(left, right)

    sorted_arr = merge_sort_recursive(arr)
    if not track_comparisons:
        # Update the original list if not tracking comparisons
        arr[:] = sorted_arr
    return comparisons if track_comparisons else sorted_arr
