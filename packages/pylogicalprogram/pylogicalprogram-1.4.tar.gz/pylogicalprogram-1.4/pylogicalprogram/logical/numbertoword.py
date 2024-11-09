def number_to_words(n):
    if n == 0:
        return 'Zero'
    units = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
             'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    thousands = ['', 'Thousand', 'Million', 'Billion', 'Trillion']
    def word(num, idx):
        if num == 0:
            return ''
        if num < 20:
            return units[num] + ' ' + thousands[idx] + ' '
        elif num < 100:
            return tens[num // 10] + ' ' + units[num % 10] + ' ' + thousands[idx] + ' '
        else:
            return units[num // 100] + ' Hundred ' + word(num % 100, 0) + thousands[idx] + ' '
    def num_to_words(num):
        if num == 0:
            return ''
        idx = 0
        words = ''
        while num > 0:
            if num % 1000 != 0:
                words = word(num % 1000, idx) + words
            num //= 1000
            idx += 1
        return words.strip()
    return num_to_words(n)