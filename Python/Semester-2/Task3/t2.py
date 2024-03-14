def decode(s):
    decoded = ""
    i = 0
    while i < len(s):
        if s[i].isalpha():
            decoded += s[i]
            i += 1
        else:
            count = ""
            while i < len(s) and s[i].isdigit():
                count += s[i]
                i += 1
            count = int(count)
            decoded += decoded[-1] * (count - 1)
    return decoded


# Пример использования:
if __name__ == '__main__':
    data = input("Enter: ")
    print(decode(data))
