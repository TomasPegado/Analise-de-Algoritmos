def LinearSelection(A, k):
    """
    Returns the k-th smallest element in list A (1-based index) using the median of medians algorithm.
    Raises ValueError if k is out of bounds.
    """
    if k <= 0 or k > len(A):
        raise ValueError("k is out of bounds")

    # Base case: small list, sort and return
    if len(A) <= 5:
        return sorted(A)[k-1]

    # Step 1: Divide A into groups of 5
    groups = []
    for i in range(0, len(A), 5):
        groups.append(A[i:i+5])

    medians = []
    for group in groups:
        median = sorted(group)[len(group)//2]
        medians.append(median)

    # Step 3: Find the median of medians
    pivot = LinearSelection(medians, len(medians)//2 + 1)

    # Step 4: Partition A into <, =, > pivot
    L = []
    E = []
    R = []
    for x in A:
        if x < pivot:
            L.append(x)
        elif x == pivot:
            E.append(x)
        else:  # x > pivot
            R.append(x)

    # Step 5: Recurse or return
    if k <= len(L):
        return LinearSelection(L, k)
    elif k <= len(L) + len(E):
        return pivot
    else:
        return LinearSelection(R, k - len(L) - len(E))

def BubbleSort(A):
    """
    Returns a sorted copy of list A using BubbleSort algorithm.
    """
    Aord = A.copy()
    n = len(Aord)
    for i in range(n):
        for j in range(0, n - i - 1):
            if Aord[j] > Aord[j + 1]:
                Aord[j], Aord[j + 1] = Aord[j + 1], Aord[j]
    return Aord

def SortSelection(A, k):
    """
    Returns the k-th smallest element in list A (1-based index) using BubbleSort.
    Raises ValueError if k is out of bounds.
    """
    if k <= 0 or k > len(A):
        raise ValueError("k is out of bounds")
    Aord = BubbleSort(A)
    return Aord[k-1]

if __name__ == "__main__":
    import random
    import time

    print("n\tLinearSelection(s)\tSortSelection(s)")
    for n in range(1000, 10001, 1000):
        lin_times = []
        sort_times = []
        for _ in range(10):
            A = [random.randint(1, 100000) for _ in range(n)]
            k = n // 2

            # Time LinearSelection
            start = time.time()
            lin_result = LinearSelection(A, k)
            lin_time = time.time() - start
            lin_times.append(lin_time)

            # Time SortSelection
            start = time.time()
            sort_result = SortSelection(A, k)
            sort_time = time.time() - start
            sort_times.append(sort_time)

            # Correctness check
            assert lin_result == sort_result, f"Mismatch for n={n}, k={k}: {lin_result} != {sort_result}"

        avg_lin = sum(lin_times) / len(lin_times)
        avg_sort = sum(sort_times) / len(sort_times)
        print(f"{n}\t{avg_lin:.6f}\t\t{avg_sort:.6f}") 