def egg_drop(eggs, floors):
    dp = [[0] * (floors + 1) for _ in range(eggs + 1)]

    # Если 1 яйцо — проверяем все этажи поочередно
    for i in range(1, floors + 1):
        dp[1][i] = i

    # Если 1 этаж — нужна 1 попытка
    for i in range(1, eggs + 1):
        dp[i][1] = 1

    # Заполняем таблицу DP
    for e in range(2, eggs + 1):
        for f in range(2, floors + 1):
            low, high = 1, f
            min_attempts = float('inf')

            # Бинарный поиск для выбора оптимального этажа
            while low <= high:
                mid = (low + high) // 2
                egg_breaks = dp[e - 1][mid - 1]  # Разбилось — идем вниз
                egg_survives = dp[e][f - mid]  # Не разбилось — идем вверх
                worst_case = 1 + max(egg_breaks, egg_survives)

                # Обновляем минимум
                min_attempts = min(min_attempts, worst_case)

                if egg_breaks > egg_survives:
                    high = mid - 1  # Ищем ниже
                else:
                    low = mid + 1  # Ищем выше

            dp[e][f] = min_attempts

    return dp[eggs][floors]


if __name__ == '__main__':
    print(egg_drop(2, 10))  # Ожидаемый ответ: 4
