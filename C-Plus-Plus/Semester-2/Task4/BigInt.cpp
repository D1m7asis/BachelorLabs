#include "BigInt.h"
#include <stdexcept>


void BigInt::removeLeadingZeros() {
    while (digits.size() > 1 && digits.back() == 0) {
        digits.pop_back();
    }
}

BigInt::BigInt() {
    digits.push_back(0);
}

BigInt::BigInt(int num) {
    if (num == 0) {
        digits.push_back(0);
        return;
    }
    while (num != 0) {
        digits.push_back(num % 10);
        num /= 10;
    }
}

/**
 * \brief  Конструктор BigInt::BigInt(const std::string& numStr)
 *
 * \Работа Цикл проходит через строку numStr в обратном порядке, начиная
 * с последнего символа и заканчивая первым (\b rbegin() возвращает итератор
 * на последний элемент, а \b rend() возвращает итератор, указывающий на позицию после последнего элемента).
 * Внутри цикла каждый символ строки преобразуется в цифру,
 * вычитая из его ASCII-кода значение '0' (ASCII код цифры '0').
 * Таким образом, символы '0' до '9' будут преобразованы в числа от 0 до 9.
 * Числа проверяются на удовлетворение следующих условию: \b положительное/отрицательное и \b корректное.
 * Эти числа затем добавляются в вектор digits (последовательность цифр числа),
 * начиная с младших разрядов и заканчивая старшими разрядами.
 * После того как все цифры добавлены, вызывается функция removeLeadingZeros(),
 * которая удаляет ведущие нули из числа (если они есть).
 **/
BigInt::BigInt(const std::string& numStr) {
    for (auto it = numStr.rbegin(); it != numStr.rend(); ++it) {
        auto digit = *it - '0';

        if (((digit > 9) || (digit < 0))) {
            if (it == --numStr.rend()) {
                digits[digits.size()-1] *= -1;
                break;
            } else {
                throw std::invalid_argument("Incorrect BigInt was been fed.");
            }
        }
        digits.push_back(digit);
    }
    removeLeadingZeros();
}

BigInt::BigInt(const BigInt& other) = default;

BigInt& BigInt::operator=(const BigInt& other) {
    if (this != &other) {
        digits = other.digits;
    }
    return *this;
}

BigInt::~BigInt() = default;

/**
 * \brief  Функция складывает два объекта типа BigInt и возвращает результат в виде нового объекта BigInt.
 *
 * \Работа Создается новый объект result, который будет содержать результат сложения.
 * Инициализируется переменная carry для хранения переноса при сложении разрядов.
 * Определяется максимальная длина числа, которое равна максимальной длине между digits текущего объекта и digits переданного объекта other.
 * Запускается цикл, который проходит через все разряды, начиная с младших и заканчивая старшими. Цикл также продолжается, если есть неучтенный перенос из предыдущих разрядов (условие || carry).
 * Внутри цикла проверяется, если i-й разряд результата уже существует (т.е. i == result.digits.size()), и если нет, он создается и инициализируется нулевым значением.
 * Вычисляется сумма для i-го разряда результата. Она состоит из переноса carry, текущего разряда объекта digits и other.digits (если они существуют).
 * Перенос вычисляется как целая часть от деления суммы на 10.
 * Остаток от деления суммы на 10 записывается как i-й разряд результата.
 * Цикл завершается, когда все разряды объектов digits и other.digits (если есть) обработаны, и нет переноса.
 **/
BigInt BigInt::operator+(const BigInt& other) const {
    BigInt result;
    int carry = 0;
    size_t maxSize = std::max(digits.size(), other.digits.size());
    for (size_t i = 0; i < maxSize || carry; ++i) {
        if (i == result.digits.size())
            result.digits.push_back(0);
        result.digits[i] += carry + (i < digits.size() ? digits[i] : 0) + (i < other.digits.size() ? other.digits[i] : 0);
        carry = result.digits[i] / 10;
        result.digits[i] %= 10;
    }

    return result;
}

BigInt& BigInt::operator+=(const BigInt& other) {
    *this = *this + other;

    removeLeadingZeros();
    return *this;
}


BigInt BigInt::operator*(const BigInt& other) const {
    BigInt result;
    std::vector<int>::size_type m = digits.size(), n = other.digits.size();
    result.digits.resize(m + n);
    for (std::vector<int>::size_type i = 0; i < m; ++i) {
        int carry = 0;
        for (std::vector<int>::size_type j = 0; j < n || carry; ++j) {
            auto sum = static_cast<long long>(result.digits[i + j]) + static_cast<long long>(digits[i]) * (j < n ? other.digits[j] : 0) + carry;
            result.digits[i + j] = static_cast<int>(sum % 10);
            carry = static_cast<int>(sum / 10);
        }
    }
    result.removeLeadingZeros();
    return result;
}

BigInt& BigInt::operator*=(const BigInt& other) {
    *this = *this * other;
    return *this;
}

bool BigInt::operator<(const BigInt& other) const {
    if (digits.size() != other.digits.size()) {
        return digits.size() < other.digits.size();
    }
    for (std::vector<int>::size_type i = digits.size(); i-- > 0;) {
        if (digits[i] != other.digits[i]) {
            return digits[i] < other.digits[i];
        }
    }
    return false;
}

bool BigInt::operator>(const BigInt& other) const {
    return other < *this;
}

bool BigInt::operator==(const BigInt& other) const {
    return digits == other.digits;
}

bool BigInt::operator!=(const BigInt& other) const {
    return !(*this == other);
}

std::ostream& operator<<(std::ostream& os, const BigInt& num) {
    for (std::vector<int>::size_type i = num.digits.size(); i-- > 0;) {
        os << num.digits[i];
    }
    return os;
}

std::istream& operator>>(std::istream& is, BigInt& num) {
    std::string input;
    is >> input;
    num = BigInt(input);
    return is;
}
