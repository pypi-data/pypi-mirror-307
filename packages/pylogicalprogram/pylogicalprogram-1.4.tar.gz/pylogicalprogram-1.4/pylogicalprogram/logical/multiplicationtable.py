
def multiplicationTableWithRange(num, tablerange):
    s = ""
    for i in range(1, tablerange + 1):
        n = num * i
        s += f"{i} * {num} = {n}\n"
    return s

def multiplicationSpecificTable(num, table):
    return num * table