def generate_acronym(sentence):
    words = sentence.split()
    acronym = ""
    for word in words:
        acronym += word[0].upper()
    return acronym

# Ввод строки от пользователя
user_input = input("Введите строку: ")
abbreviation = generate_acronym(user_input)
print("Аббревиатура:", abbreviation)
