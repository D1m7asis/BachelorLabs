def count_string_repetitions(data):
    counts = {}
    strs = ''

    for string in data:
        if string in counts:
            counts[string] += 1
        else:
            counts[string] = 1

    for s in counts.values():
        strs += f"{s} "
    return strs


if __name__ == '__main__':
    input_data = [
        ['abc', 'bcd', 'abc', 'abd', 'abd', 'dcd', 'abc'],
        ['aaa', 'bbb', 'ccc'],
        ['abc', 'abc', 'abc']
    ]

    for strings in input_data:
        repetitions = count_string_repetitions(strings)
        print(repetitions)
