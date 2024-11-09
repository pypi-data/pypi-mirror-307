
def swapTwoNumWithTemp(num1, num2):
    temp = num1
    num1 = num2
    num2 = temp
    return num1, num2

def swapTwoNumWithoutTemp(num1, num2):
    num2 = num1 + num2
    num1 = num2 - num1
    num2 = num2 - num1
    return num1, num2