
def generateParenthesis(n):
    parenthesis_list = []
    def parentheses(s, left, right, parenthesis_list):
        if left > right: return
        if left == 0 and right == 0:
            parenthesis_list.append(s)
            return
        if left > 0:
            parentheses(s+"(", left-1, right, parenthesis_list)
        if right > 0:
            parentheses(s+")", left, right-1, parenthesis_list)
    parentheses("", n, n, parenthesis_list)
    return parenthesis_list