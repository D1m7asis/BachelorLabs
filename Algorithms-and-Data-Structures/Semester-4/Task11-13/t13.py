from functools import lru_cache


def bin_packing_dp(items, bin_capacity):
    n = len(items)
    all_items = (1 << n) - 1  # Все предметы включены

    @lru_cache(None)
    def dp(mask):
        if mask == 0:
            return 0
        min_bins = n
        subset = mask
        while subset:
            weight = sum(items[i] for i in range(n) if subset & (1 << i))
            if weight <= bin_capacity:
                min_bins = min(min_bins, 1 + dp(mask ^ subset))
            subset = (subset - 1) & mask
        return min_bins

    return dp(all_items)


items = [4, 8, 1, 4, 2, 1]
bin_capacity = 10
print("Минимальное количество ящиков (DP):", bin_packing_dp(tuple(items), bin_capacity))
