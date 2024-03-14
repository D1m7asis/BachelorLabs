def encode(s):
    encoded = ""
    count = 1
    for i in range(len(s)):
        if i < len(s) - 1 and s[i] == s[i + 1]:
            count += 1
        else:
            if count > 1:
                encoded += s[i] + str(count)
            else:
                encoded += s[i]
            count = 1
    return encoded


if __name__ == '__main__':
    data = input("Enter: ")
    print(encode(data))
