#ifndef BIGINT_H
#define BIGINT_H

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

class BigInt {
private:
    std::vector<int> digits;
    void removeLeadingZeros();

public:
    BigInt();
    explicit BigInt(int num);
    explicit BigInt(const std::string& numStr);
    BigInt(const BigInt& other);
    BigInt& operator=(const BigInt& other);
    ~BigInt();

    BigInt operator+(const BigInt& other) const;
    BigInt& operator+=(const BigInt& other);

    BigInt operator*(const BigInt& other) const;
    BigInt& operator*=(const BigInt& other);

    bool operator<(const BigInt& other) const;
    bool operator>(const BigInt& other) const;
    bool operator==(const BigInt& other) const;
    bool operator!=(const BigInt& other) const;

    friend std::ostream& operator<<(std::ostream& os, const BigInt& num);
    friend std::istream& operator>>(std::istream& is, BigInt& num);
};

#endif // BIGINT_H
