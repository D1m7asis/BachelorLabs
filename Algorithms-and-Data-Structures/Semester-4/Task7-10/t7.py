from typing import List


def max_subarray(nums: List[int]) -> int:
    """
    Находит сумму непрерывного подмассива с наибольшей суммой в списке nums
    с использованием алгоритма Кадана.

    Аргументы:
      nums: Список целых чисел.

    Возвращает:
      Целое число – максимальную сумму непрерывного подмассива.
    """
    if not nums:
        raise ValueError("Список не должен быть пустым.")

    # Инициализируем максимальную сумму как первый элемент.
    max_current = max_global = nums[0]

    # Проходим по элементам начиная со второго.
    for num in nums[1:]:
        # Решаем, начинать новый подмассив с текущим элементом или продолжать существующий.
        max_current = max(num, max_current + num)
        # Обновляем глобальный максимум, если нашли большую сумму.
        if max_current > max_global:
            max_global = max_current

    return max_global


if __name__ == '__main__':
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    print("Максимальная сумма подмассива:", max_subarray(nums))
