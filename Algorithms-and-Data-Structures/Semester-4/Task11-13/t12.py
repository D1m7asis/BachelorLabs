def knapsack_recursive(items, W, n, memo={}):
    if n == 0 or W == 0:
        return 0

    if (n, W) in memo:
        return memo[(n, W)]

    weight, value = items[n - 1]

    # Если вес превышает текущий лимит, пропускаем предмет
    if weight > W:
        memo[(n, W)] = knapsack_recursive(items, W, n - 1, memo)
        return memo[(n, W)]

    # Выбираем максимум между:
    # 1️⃣ Не берём предмет
    # 2️⃣ Берём предмет и уменьшаем вместимость
    memo[(n, W)] = max(
        knapsack_recursive(items, W, n - 1, memo),
        value + knapsack_recursive(items, W - weight, n - 1, memo),
    )
    return memo[(n, W)]


items = [(15, 2), (13, 5), (13, 9), (12, 5), (12, 9), (11, 7)]
W = 100

print("Максимальная ценность:", knapsack_recursive(items, W, len(items)))
