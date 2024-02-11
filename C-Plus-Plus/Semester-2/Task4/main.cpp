#include "BigInt.h"

int main() {
    BigInt a   ("123456789012345678901234567890");
    BigInt b   ("987654321098765432109876543210");
    BigInt sum("1111111110111111111011111111100");

    BigInt sumPredict = a + b;
    std::cout << "Sum is equal? " << ((sum==sumPredict) ? "True" : "False") << std::endl;

    sum += (sumPredict *= BigInt(-1));
    std::cout << "sum - sumPredict is: " << sum << std::endl;

    BigInt c ("1100");
    BigInt d ("1000");

    if (c != d) {
        std::cout << "The biggest from c & d is: " << (c > d ? "c" : "d") << std::endl;
    }

    std::cout << "c & d is: " << (c == d ? "Equal" : "Not equal") << std::endl;

    std::cout << c << std::endl;
    c += BigInt("-100");
    std::cout << c << std::endl;

    std::cout << "c & d is: " << (c == d ? "Equal" : "Not equal") << std::endl;

    return 0;
}