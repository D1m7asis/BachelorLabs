def comb_sort(arr):
    n = len(arr)
    gap = n
    shrink = 1.3  # Коэффициент уменьшения зазора
    sorted = False

    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        i = 0
        while i + gap < n:
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted = False
            i += 1


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]


def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2


def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr):
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort(arr, exp)
        exp *= 10


def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l] > arr[largest]:
        largest = l

    if r < n and arr[r] > arr[largest]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def external_sort(arr, chunk_size):
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]

    for i in range(len(chunks)):
        chunks[i] = sorted(chunks[i])

    sorted_arr = []
    while any(chunks):
        min_chunk = min((chunk for chunk in chunks if chunk), key=lambda x: x[0])
        sorted_arr.append(min_chunk.pop(0))
        chunks = [chunk for chunk in chunks if chunk]

    return sorted_arr


def main():
    arr = list(map(int, input("Введите числа для сортировки: ").split()))

    print("\nСортировка методом прочесывания:")
    arr_comb = arr.copy()
    comb_sort(arr_comb)
    print(arr_comb)

    print("\nСортировка вставками:")
    arr_insertion = arr.copy()
    insertion_sort(arr_insertion)
    print(arr_insertion)

    print("\nСортировка выбором:")
    arr_selection = arr.copy()
    selection_sort(arr_selection)
    print(arr_selection)

    print("\nСортировка Шелла:")
    arr_shell = arr.copy()
    shell_sort(arr_shell)
    print(arr_shell)

    print("\nПоразрядная сортировка:")
    arr_radix = arr.copy()
    radix_sort(arr_radix)
    print(arr_radix)

    print("\nПирамидальная сортировка:")
    arr_heap = arr.copy()
    heap_sort(arr_heap)
    print(arr_heap)

    print("\nСортировка слиянием:")
    arr_merge = arr.copy()
    merge_sort(arr_merge)
    print(arr_merge)

    print("\nБыстрая сортировка:")
    arr_quick = arr.copy()
    sorted_quick = quick_sort(arr_quick)
    print(sorted_quick)

    print("\nВнешняя многофазная сортировка:")
    arr_external = arr.copy()
    chunk_size = 5
    sorted_external = external_sort(arr_external, chunk_size)
    print(sorted_external)


if __name__ == "__main__":
    main()
