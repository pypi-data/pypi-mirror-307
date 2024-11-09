
def integerToRoman(num):
    def intToRom():
        dict = {}
        dict[1000] = "M"
        dict[900] = "CM"
        dict[500] = "D"
        dict[400] = "CD"
        dict[100] = "C"
        dict[90] = "XC"
        dict[50] = "L"
        dict[40] = "XL"
        dict[10] = "X"
        dict[9] = "IX"
        dict[5] = "V"
        dict[4] = "IV"
        dict[1] = "I"
        return dict
    string = ""
    for key in intToRom().keys():
        while key<=num:
            num -= key
            string += intToRom()[key]
    return string