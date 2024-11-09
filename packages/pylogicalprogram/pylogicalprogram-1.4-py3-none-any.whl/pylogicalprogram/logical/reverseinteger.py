
def reverseInteger(num):
    sum = 0
    n = num
    while 0 < num:
        r = num % 10
        sum = (sum * 10) + r
        num = num // 10
    return n == sum

def reverseIntegerWithSigned(num):
    s = str(num)
    if s[0] == '-':
        n = s[:0:-1]
        return int(-int(n))
    else:
        return int(s[::-1])
