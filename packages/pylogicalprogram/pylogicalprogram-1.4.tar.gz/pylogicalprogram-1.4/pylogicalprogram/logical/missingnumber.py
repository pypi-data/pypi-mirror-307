
def missingNumber(nums):
    l = len(nums) + 1
    s = l * (l + 1) // 2
    t = sum(nums)
    return s - t