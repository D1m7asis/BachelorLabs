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
                return False

    return not stack


def to_rpn(mth_ex):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    output = []
    operators = []
    i = 0

    while i < len(mth_ex):
        char = mth_ex[i]

        # Распознаем отрицательные числа
        if char == '-' and (i == 0 or mth_ex[i - 1] in '(-+*/'):
            number = char
            i += 1
            while i < len(mth_ex) and mth_ex[i].isdigit():
                number += mth_ex[i]
                i += 1
            output.append(number)
            continue

        if char.isdigit():
            number = char
            while i + 1 < len(mth_ex) and mth_ex[i + 1].isdigit():
                i += 1
                number += mth_ex[i]
            output.append(number)
        elif char in precedence:
            while (operators and operators[-1] in precedence and
                   precedence[operators[-1]] >= precedence[char]):
                output.append(operators.pop())
            operators.append(char)
        elif char == '(':
            operators.append(char)
        elif char == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            operators.pop()  # удаляем '('
        i += 1

    while operators:
        output.append(operators.pop())

    return output


def evaluate_rpn(rpn):
    stack = []

    for token in rpn:
        if token.lstrip('-').isdigit():  # Учитываем отрицательные числа
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()

            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                stack.append(a / b)

    return stack[0]


def evaluate_expression(mth_ex):
    mth_ex = mth_ex.replace('=', '')

    # Проверка скобок
    if not is_brackets_correct(mth_ex):
        print("Некорректные скобки в выражении")
        return

    try:
        rpn = to_rpn(mth_ex)
        result = evaluate_rpn(rpn)
        print("Результат:", result)
    except ZeroDivisionError as e:
        print(e)
    except Exception as e:
        print("Ошибка:", e)


if __name__ == '__main__':
    expression = input("Введите математическое выражение: ")
    evaluate_expression(expression)
