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

    if not stack:
        return True
    else:
        return False


def evaluate_expression_with_eval(expression):
    expression = expression.replace('=', '')

    if not is_brackets_correct(expression):
        print("Некорректные скобки в выражении")
        return

    try:
        if not all(char.isdigit() or char in "+-*/(). " for char in expression):
            raise ValueError("Недопустимые символы в выражении")

        result = eval(expression)  # :-P

        print("Результат:", result)
    except ZeroDivisionError:
        print("Ошибка: Деление на ноль")
    except Exception as e:
        print("Ошибка:", e)


if __name__ == '__main__':
    expression = input("Введите математическое выражение: ")
    evaluate_expression_with_eval(expression)
