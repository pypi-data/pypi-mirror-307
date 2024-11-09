
def spiralMatrixWithList(l):
    matrix_list = []
    if len(l) == 0:
        return matrix_list
    row1 = 0
    row2 = len(l) - 1
    column1 = 0
    column2 = len(l[0]) - 1
    while row1 <= row2 and column1 <= column2:
        for i in range(column1, column2 + 1):
            matrix_list.append(l[row1][i])
        for i in range(row1 + 1, row2 + 1):
            matrix_list.append(l[i][column2])
        if row1 < row2 and column1 < column2:
            for i in range(column2 - 1, column1, -1):
                matrix_list.append(l[row2][i])
            for i in range(row2, row1, -1):
                matrix_list.append(l[i][column1])
        row1 = row1 + 1
        row2 = row2 - 1
        column1 = column1 + 1
        column2 = column2 - 1
    return matrix_list

def spiralMatrixWithInt(n):
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    num = 1
    top, bottom, left, right = 0, n - 1, 0, n - 1
    while num <= (n * n):
        for i in range(left, right + 1):
            matrix[top][i] = num
            num = num + 1
        top = top + 1
        for i in range(top, bottom + 1):
            matrix[i][right] = num
            num = num + 1
        right = right - 1
        for i in range(right, left - 1, -1):
            matrix[bottom][i] = num
            num = num + 1
        bottom = bottom - 1
        for i in range(bottom, top - 1, -1):
            matrix[i][left] = num
            num = num + 1
        left = left + 1
    return matrix
