
def stringReverse1(string):
    return string[::-1]

def stringReverse2(string):
    s = ""
    for i in range(len(string)-1, -1, -1):
        s += string[i]
    return s==string

def stringPalindrome(string):
    return string == string[::-1]
def numberPalindrome(numeber):
    n = numeber
    sum = 0
    while 0 < numeber:
        r = numeber % 10
        sum = (sum * 10) + r
        numeber = numeber // 10
    return n == sum