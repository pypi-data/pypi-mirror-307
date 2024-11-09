# Square Pattern
def Square_Pattern(num, pattern_type='star'):
    for i in range(1, num+1):
        for j in range(1, num+1):
            if pattern_type == 'star': print('*', end=" ")
            if pattern_type == 'i': print(i, end=" ")
            if pattern_type == 'j': print(j, end=" ")
        print()

# Hollow Square Pattern
def Hollow_Square_Pattern(num, pattern_type='star'):
    for i in range(1, num+1):
        for j in range(1, num+1):
            if i == 1 or i == num+1 - 1 or j == 1 or j == num+1 - 1:
                if pattern_type == 'star': print('*', end=" ")
                if pattern_type == 'i': print(i, end=" ")
                if pattern_type == 'j': print(j, end=" ")
            else:
                print(' ', end=' ')
        print()

# Hollow Square Pattern With Cross
def Square_With_Cross_Pattern(num, pattern_type='star'):
    for i in range(1, num+1):
        for j in range(1, num+1):
            if i==1 or j==1 or i==num or j==num or i==j or i+j==num+1:
                if pattern_type == 'star': print('* ', end=" ")
                if pattern_type == 'i': print(i, end="  ")
                if pattern_type == 'j': print(j, end="  ")
            else:
                print(end="   ")
        print()

# Left Triangle Star Pattern
def Left_Triangle_Star_Pattern(num, pattern_type='star'):
    for i in range(1, num + 1):
        for j in range(1, i + 1):
            if pattern_type == 'star': print('*', end=" ")
            if pattern_type == 'i': print(i, end=" ")
            if pattern_type == 'j': print(j, end=" ")
        print()

# Left Downward Triangle Pattern
def Left_Downward_Triangle_Pattern(num, pattern_type='star'):
    for i in range(1, num + 1):
        for j in range(1, num - i + 2):
            if pattern_type == 'star': print('*', end=" ")
            if pattern_type == 'i': print(i, end=" ")
            if pattern_type == 'j': print(j, end=" ")
        print()

# Right Triangle Star Pattern
def Right_Triangle_Star_Pattern(num, pattern_type='star'):
    for i in range(1, num + 1):
        for j in range(0, num - i):
            print(' ', end=" ")
        for j in range(1, i + 1):
            if pattern_type == 'star': print('*', end=" ")
            if pattern_type == 'i': print(i, end=" ")
            if pattern_type == 'j': print(j, end=" ")
        print()

# Right Downward Triangle Pattern
def Right_Downward_Triangle_Pattern(num, pattern_type='star'):
    for i in range(1, num + 1):
        for j in range(num - i, num):
            print(' ', end=" ")
        for j in range(1, num - i + 2):
            if pattern_type == 'star': print('*', end=" ")
            if pattern_type == 'i': print(i, end=" ")
            if pattern_type == 'j': print(j, end=" ")
        print()

# Hollow triangle Pattern
def Hollow_Triangle_Star_Pattern(num, pattern_type='star'):
    for i in range(1, num+1):
        for j in range(i):
            if j == 0 or j == i - 1:
                if pattern_type == 'star': print('*', end=" ")
                if pattern_type == 'i': print(i, end=" ")
                if pattern_type == 'j': print(j, end=" ")
            else:
                if i != num:
                    print(' ', end=' ')
                else:
                    if pattern_type == 'star': print('*', end=" ")
                    if pattern_type == 'i': print(i, end=" ")
                    if pattern_type == 'j': print(j, end=" ")
        print()

# Pyramid Pattern
def Pyramid_Pattern(num, pattern_type='star'):
    for i in range(1, num+1):
        for j in range(1, num + 1 - i):
            print(end="  ")
        for j in range(1, i+1):
            if pattern_type == 'star': print('*', end=" ")
            if pattern_type == 'i': print(i, end=" ")
            if pattern_type == 'j': print(j, end=" ")
        for j in range(1, i):
            if pattern_type == 'star': print('*', end=" ")
            if pattern_type == 'i': print(i, end=" ")
            if pattern_type == 'j': print(j, end=" ")
        print()

# Reverse Pyramid Pattern
def Reverse_Pyramid_Pattern(num, pattern_type='star'):
    for i in range(1, num+1):
        for j in range(num - i, num):
            print(' ', end=" ")
        for j in range(1, num+2 - i):
            if pattern_type == 'star': print('*', end=" ")
            if pattern_type == 'i': print(i, end=" ")
            if pattern_type == 'j': print(j, end=" ")
        for j in range(1, num+1 - i):
            if pattern_type == 'star': print('*', end=" ")
            if pattern_type == 'i': print(i, end=" ")
            if pattern_type == 'j': print(j, end=" ")
        print()

# Right Pascal Pattern
def Right_Pascal_Star_Pattern(num, pattern_type='star'):
    for i in range(1, num+1):
        for j in range(1, i+1):
            if pattern_type == 'star': print('*', end=" ")
            if pattern_type == 'i': print(i, end=" ")
            if pattern_type == 'j': print(j, end=" ")
        print("\r")
    for i in range(1, num+1):
        for j in range(num - 1 - i, - 1, -1):
            if pattern_type == 'star': print('*', end=" ")
            if pattern_type == 'i': print(i, end=" ")
            if pattern_type == 'j': print(j, end=" ")
        print()

# Left Pascal Pattern
def Left_Pascal_Star_Pattern(num, pattern_type='star'):
    for i in range(1, num+1):
        for j in range(1, num + 1 - i):
            print(end="   ")
        for j in range(1, i+1):
            print(" * ", end="")
        print("\r")
    for i in range(1, num+1):
        for j in range(0, i):
            print(end="   ")
        for j in range(0, num-i):
            print(" * ", end="")
        print("\r")

# Hollow Pyramid Pattern
def Hollow_Pyramid_Pattern(num, pattern_type='star'):
    n = num
    for i in range(1, n + 1):
        for j in range(n - i):
            print(' ', end=' ')
        for k in range(2 * i - 1):
            if k == 0 or k == 2 * i - 2:
                print('*', end='')
            else:
                if i == n:
                    print('*', end=' ')
                else:
                    print(' ', end=' ')
        print()

# Plus Pattern
def Plus_Pattern(num, pattern_type='star'):
    for i in range(1, 2*num):
        for j in range(1, 2*num):
            if j==num or i==num:
                print("*", end=" ")
            else:
                print(' ', end=' ')
        print()

# Cross_Pattern
def Cross_Pattern(num, pattern_type='star'):
    for i in range(1, num+1):
        for j in range(1, num+1):
            if i==j or i+j==num+1:
                if pattern_type == 'star': print('*', end=" ")
                if pattern_type == 'i': print(i, end=" ")
                if pattern_type == 'j': print(j, end=" ")
            else:
                print(end="   ")
        print()

# Heart_Pattern
def Heart_Pattern(num):
    for i in range(num // 2, num, 2):
        for j in range(1, num - i, 2):
            print(" ", end=" ")
        for j in range(1, i + 1, 1):
            print("*", end=" ")
        for j in range(1, num - i + 1, 1):
            print(" ", end=" ")
        for j in range(1, i + 1, 1):
            print("*", end=" ")
        print()
    for i in range(num, 0, -1):
        for j in range(i, num, 1):
            print(" ", end=" ")
        for j in range(1, i * 2, 1):
            print("*", end=" ")
        print()

def Diamond_Star_Pattern(num):
    n = num
    for i in range(n):
        for j in range(n - i - 1):
            print(' ', end=' ')
        for j in range(2 * i + 1):
            print('*', end=' ')
        print()
    for i in range(n - 1):
        for j in range(i + 1):
            print(' ', end=' ')
        for j in range(2 * (n - i - 1) - 1):
            print('*', end=' ')
        print()

def Hollow_Diamond_Star_Pattern(num):
    n = num
    for i in range(n):
        for j in range(n - i - 1):
            print(' ', end='')
        for j in range(2 * i + 1):
            if j == 0 or j == 2 * i:
                print('*', end='')
            else:
                print(' ', end='')
        print()
    for i in range(n - 1):
        for j in range(i + 1):
            print(' ', end='')
        for j in range(2 * (n - i - 1) - 1):
            if j == 0 or j == 2 * (n - i - 1) - 2:
                print('*', end='')
            else:
                print(' ', end='')
        print()

def Hourglass_Star_Pattern(num):
    n = num
    for i in range(n - 1):
        for j in range(i):
            print(' ', end=' ')
        for k in range(2 * (n - i) - 1):
            print('*', end=' ')
        print()
    for i in range(n):
        for j in range(n - i - 1):
            print(' ', end=' ')
        for k in range(2 * i + 1):
            print('*', end=' ')
        print()
