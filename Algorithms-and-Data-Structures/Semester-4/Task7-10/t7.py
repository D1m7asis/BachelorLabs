from typing import List


def maxSubArray(nums: List[int]) -> int:
    if len(nums) < 2:
        return nums[0]

    for i in range(1, len(nums)):
        if nums[i - 1] > 0:
            nums[i] += nums[i - 1]

    return max(nums)


if __name__ == '__main__':
    print(maxSubArray([-2, 1, -3, 4, -1, 2]))
