
def fibonacciSeries(num):
    f1 = 0
    f2 = 1
    f3 = 0
    for i in range(1, num):
        f3 = f1 + f2
        f1 = f2
        f2 = f3
    return f3

def fibonacciSeriesWithRecurtion(num):
    if num <= 1:
        return num
    return fibonacciSeriesWithRecurtion(num - 1) + fibonacciSeriesWithRecurtion(num - 2)
