def numberDigitCount(n):
    sum = n
    while n > 9:
        sum = 0
        while 0 < n:
            r = n % 10
            sum += r
            n //= 10
        n = sum
    return sum

def NumberDigitCountRecursion(n):
    if n<=9:
        return n
    sum = 0
    while 0 < n:
        r = n % 10
        sum = sum + r
        n //= 10
    return NumberDigitCountRecursion(sum)
