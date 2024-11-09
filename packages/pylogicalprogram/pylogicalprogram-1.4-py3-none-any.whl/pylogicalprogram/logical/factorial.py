def factorialwithRecursion(num):
    if num == 0:
        return 1
    return num * factorialwithRecursion(num - 1)

def factorial(num):
    n = 1
    for i in range(1, num + 1):
        n *= i
    return n