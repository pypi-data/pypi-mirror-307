import itertools
def permutationsInt(nums):
    perm = itertools.permutations(nums)
    return [list(p) for p in perm]

def permutationsIntWithLen(nums, length):
    perm = itertools.permutations(nums, length)
    return [list(p) for p in perm]

def permutationsStr(string):
    perm = itertools.permutations(string)
    return [list(p) for p in perm]

def permutationsStrWithLen(string, length):
    perm = itertools.permutations(string, length)
    return [list(p) for p in perm]
