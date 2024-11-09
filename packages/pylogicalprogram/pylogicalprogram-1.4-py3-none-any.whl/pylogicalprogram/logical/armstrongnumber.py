
def armstrongNumber(num):
    n = num
    sum = 0
    l = len(str(num))
    while 0 < num:
        r = num % 10
        sum += r ** l
        num = num // 10
    return n == sum