def is_brackets_correct(brackets: str) -> bool:
    stack = []
    bracket_pairs = {')': '(',
                     '}': '{',
                     ']': '['}

    for char in brackets:
        if char in bracket_pairs.values():
            stack.append(char)

        elif char in bracket_pairs.keys():
            if stack and stack[-1] == bracket_pairs[char]:
                stack.pop()
            else:
                print("Строка не существует")
                return False

    if not stack:
        print("Строка существует")
        return True
    else:
        print("Строка не существует")
        return False


if __name__ == '__main__':
    is_brackets_correct(input("Введите строку: "))
