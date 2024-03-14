def number_to_text(num):
    units = ['', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять']
    tens = ['', 'десять', 'двадцать', 'тридцать', 'сорок', 'пятьдесят', 'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто']
    teens = ['', 'одиннадцать', 'двенадцать', 'тринадцать', 'четырнадцать', 'пятнадцать', 'шестнадцать', 'семнадцать', 'восемнадцать', 'девятнадцать']
    hundreds = ['', 'сто', 'двести', 'триста', 'четыреста', 'пятьсот', 'шестьсот', 'семьсот', 'восемьсот', 'девятьсот']

    if num < 1 or num > 1000:
        return "Число должно быть в диапазоне от 1 до 1000"

    # Разбиение числа на разряды
    ones = num % 10
    tens_place = (num // 10) % 10
    hundreds_place = (num // 100) % 10
    thousands_place = num // 1000

    result = ""
    if thousands_place:
        result += units[thousands_place] + ' тысяч '
    if hundreds_place:
        result += hundreds[hundreds_place] + ' '
    if tens_place == 1:
        result += teens[ones]
    else:
        result += tens[tens_place] + ' ' + units[ones]

    return result.strip()


if __name__ == '__main__':
    try:
        number = int(input("Введите число от 1 до 1000: "))
        print(number_to_text(number))
    except ValueError:
        print("Ошибка: Введите целое число.")
