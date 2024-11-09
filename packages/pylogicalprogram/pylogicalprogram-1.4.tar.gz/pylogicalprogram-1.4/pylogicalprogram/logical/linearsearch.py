
def linearSearch(arr, target):
    for i in range(0, len(arr)):
        if target == arr[i]:
            return i
    return -1
