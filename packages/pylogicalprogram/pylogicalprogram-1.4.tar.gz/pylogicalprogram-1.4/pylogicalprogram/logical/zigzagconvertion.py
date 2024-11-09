
def zigzagconvertion(s, numRows):
    if numRows == 1:
        return s
    string = ""
    for i in range(0, numRows):
        j = i
        f = 1
        while j<len(s):
            string += s[j]
            if i==0 or i==numRows-1:
                j += (numRows - 1) * 2
            elif f % 2 != 0:
                j += (numRows - 1) * 2 - (2 * i)
            else:
                j += (2 * i)
            f = f + 1
    return string