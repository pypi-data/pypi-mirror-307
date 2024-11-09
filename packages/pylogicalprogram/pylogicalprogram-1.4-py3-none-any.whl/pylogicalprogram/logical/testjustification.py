
def justify_text(words, width):
    result, line, line_length = [], [], 0
    for word in words:
        if line_length + len(word) + len(line) > width:
            for i in range(width - line_length):
                line[i % (len(line) - 1 or 1)] += ' '
            result.append(''.join(line))
            line, line_length = [], 0
        line.append(word)
        line_length += len(word)
    result.append(' '.join(line).ljust(width))
    return result
