#include <iostream>
#include <cstring>
#include <stdexcept>


class String {
    char* chars{};
    size_t size;

    friend std::istream& operator>>(std::istream& input, String& string);

    void createStr(size_t len) {
        chars = new char[len];
    }

    void deleteStr() {
        delete[] chars;
    }

    char* copyStr() {
        char* copy = new char[size];
        size_t c_string_len = strlen(chars) + 1;
        std::copy(chars, chars + c_string_len, copy);
        return copy;
    }

    void copyToStr(const char* c_string) {
        size_t c_string_len = strlen(c_string) + 1;
        std::copy(c_string, c_string + c_string_len, chars);
    }

public:
    String() {
        chars = {};
        size = 0;
    }

    explicit String(const char* c_string) {
        size = std::strlen(c_string) + 1;

        createStr(size);
        copyToStr(c_string);
    }

    ~String() {
        deleteStr();
    }

    String(const String& other) : String(other.chars) {}

    String& operator=(const String& other) {
        if(this == &other) {
            return *this;
        }

        deleteStr();

        createStr(other.size);
        copyToStr(other.chars);

        return *this;
    }

    String operator+(const String& other) {
        size += other.size - 1;

        auto new_c_string = copyStr();
        deleteStr();

        chars = new_c_string;
        strcat(chars, other.chars);

        return *this;
    }

    String operator+=(const String& other) {
        *this = *this + other;
        return *this;
    }


    char& operator[](size_t index) {
        return at(index);
    }

    char& at(size_t index) {
        if (index >= (size - 1)) throw std::out_of_range("Index out of range");

        return chars[index];
    }

    bool operator==(const String& other){
        return strcmp(chars, other.chars) == 0;
    }

    bool operator<(const String& other) {
        return strcmp(chars, other.chars) < 0;
    }

    bool operator>(const String& other) {
        return !(*this < other) && !(*this == other);
    }

    bool operator!=(const String& other){
        return !(*this == other);
    }

    size_t find(const char char_){
        char* pointer = strchr(chars, char_);
        if (pointer == nullptr) {
            return -1;
        }

        return (pointer - chars);
    }

    [[nodiscard]] size_t length() const {
        return (size - 1);
    }

    [[nodiscard]] const char* toChar() const {
        return chars;
    }
};

std::istream& operator>>(std::istream& input, String& string) {
std::cin >> string.size >> string.chars;
return input;
}

std::ostream& operator<<(std::ostream& output, const String& string) {
    return (output << string.toChar());
}


int main() {
    String a("C++");
    String b("Java");
    String c("Python");
    String bar(" + ");

    std::cout << (a + bar + b) << " - Old School" << std::endl;

    String d = b;
    d += bar;
    d += c;

    std::cout << d << " - New School" << std::endl;

    d = a;
    d[1] = '-';
    d[2] = '-';
    d += c;


    std::cout << d << " - Smth Cool" << std::endl;

    std::cout << a[0] << " - Hard Rock" << std::endl;

    std::cout << String("Python > C++ ? - ") << ((c > a) ? "True" : "False") << String(" - `cause Py`s string length is a little bit longer..") << std::endl;

    try {
        std::cout << a[999];
    } catch (std::out_of_range& e) {
        std::cout << e.what() << ", `cause we tried to access the 999`th el), but the str len is: " << a.length() << std::endl;
    }

    return 0;
}