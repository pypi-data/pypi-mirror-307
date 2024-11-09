size = 7

class NumbersPattern():

    def print_0(self):
        start = 1
        end = size + 1
        num_0 = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if (i==size and start<j and j<size) or (i==start and start<j and j<size) or (j==start and start<i and i<size) or (j==size and start<i and size>i):
                    line += "* "
                else:
                    line += "  "
            num_0.append(line)
        return num_0

    def print_1(self):
        start = 1
        end = size + 1
        middle = end // 2
        num_1 = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if i == size or j == middle + 1 or (j == size - i - 1 and i <= middle):
                    line += "* "
                else:
                    line += "  "
            num_1.append(line)
        return num_1

    def print_2(self):
        start = 1
        end = size + 1
        middle = end // 2
        num_2 = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if i == start or i == middle or i == size or (j == start and i >= middle) or (
                        j == size and i <= middle):
                    line += "* "
                else:
                    line += "  "
            num_2.append(line)
        return num_2

    def print_3(self):
        start = 1
        end = size + 1
        middle = end // 2
        num_3 = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if (i == size and start < j and j < size) or (i == start and start < j and j < size) or (
                        j == size and start < i and size > i) \
                        or (i == middle and j >= middle):
                    line += "* "
                else:
                    line += "  "
            num_3.append(line)
        return num_3

    def print_4(self):
        start = 1
        end = size + 1
        middle = end // 2
        num_4 = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if i == middle + 1 or j == middle + 1 or (j == middle - i + 1):
                    line += "* "
                else:
                    line += "  "
            num_4.append(line)
        return num_4

    def print_5(self):
        start = 1
        end = size + 1
        middle = end // 2
        num_5 = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if i == start or i == middle or i == size or (j == start and i <= middle) or (j == size and i >= middle):
                    line += "* "
                else:
                    line += "  "
            num_5.append(line)
        return num_5

    def print_6(self):
        start = 1
        end = size + 1
        middle = end // 2
        num_6 = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if (i == size and start < j and j < end) or (i == start and start < j and j < end) or (
                        j == start and start < i and i < size) or i == middle or (j == size and middle <= i):
                    line += "* "
                else:
                    line += "  "
            num_6.append(line)
        return num_6

    def print_7(self):
        start = 1
        end = size + 1
        middle = end // 2
        num_7 = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if i == start or j == size or (i == middle and middle <= j):
                    line += "* "
                else:
                    line += "  "
            num_7.append(line)
        return num_7

    def print_8(self):
        start = 1
        end = size + 1
        middle = end // 2
        num_8 = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if (i == size and start < j and j < size) or (i == start and start < j and j < size) or (
                        j == start and start < i and i < size) or (j == size and start < i and size > i) or i == middle:
                    line += "* "
                else:
                    line += "  "
            num_8.append(line)
        return num_8

    def print_9(self):
        start = 1
        end = size + 1
        middle = end // 2
        num_9 = []
        for i in range(start, end):
            line = ""
            for j in range(start, end):
                if i == start or i == size or j == size or i == middle or (j == start and middle >= i):
                    line += "* "
                else:
                    line += "  "
            num_9.append(line)
        return num_9

number = NumbersPattern()

def print_number(num):
    num = str(num)
    name_lines = [""] * size
    for n in num:
        method = getattr(number, f"print_{n}", None)
        if method:
            letter_lines = method()
            for i in range(size):
                name_lines[i] += letter_lines[i] + " "
    return "\n".join(name_lines)
