"""
Main __init__.py for pylogicalprogram.
Provides easy access to logical and pattern functions.
"""

# Importing necessary modules and functions from sub-packages
from .logical import *
from .patterns import *
from .shift import *
from .systeminfo import *
from .pythoninfo import *

__version__ = '1.4'
__author__ = 'rdinesh808'


# methods names
__all__ = ['numberDigitCount', 'NumberDigitCountRecursion', 'factorial', 'multiplicationTableWithRange',
           'multiplicationSpecificTable', 'integerToRoman', 'number_to_words', 'binarySearch', 'swapTwoNumWithTemp',
           'swapTwoNumWithoutTemp', 'zigzagconvertion', 'missingNumber', 'linearSearch', 'stringReverse1', 'stringReverse2',
           'stringPalindrome', 'numberPalindrome', 'fibonacciseries', 'fibonacciSeriesWithRecurtion', 'armstrongNumber',
           'romanToInteger', 'permutationsInt', 'permutationsIntWithLen', 'permutationsStr', 'permutationsStrWithLen',
           'spiralMatrixWithList', 'spiralMatrixWithInt', 'numIslands', 'generateParenthesis', 'reverseInteger',
           'reverseIntegerWithSigned', 'justify_text', 'left_shift', 'right_shift', 'Square_Pattern',
           'Hollow_Square_Pattern', 'Square_With_Cross_Pattern', 'Left_Triangle_Star_Pattern', 'Left_Downward_Triangle_Pattern',
           'Right_Triangle_Star_Pattern', 'Right_Downward_Triangle_Pattern', 'Hollow_Triangle_Star_Pattern', 'Pyramid_Pattern',
           'Reverse_Pyramid_Pattern', 'Right_Pascal_Star_Pattern', 'Left_Pascal_Star_Pattern', 'Hollow_Pyramid_Pattern',
           'Plus_Pattern', 'Cross_Pattern', 'Heart_Pattern', 'Diamond_Star_Pattern', 'Hollow_Diamond_Star_Pattern',
           'Hourglass_Star_Pattern', 'get_system_info', 'get_memory_info', 'get_network_info', 'get_battery_info', 'get_disk_info',
           'get_cpu_info', 'get_python_info', 'get_python_paths', 'get_virtual_env_info', 'get_installed_packages']
