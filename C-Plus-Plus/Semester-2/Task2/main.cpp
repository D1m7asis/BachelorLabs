#include <iostream>
#include "Matrix.hpp"

void print(const Matrix& m)
{
    for (int i = 0; i < m.rowCount(); i++)
    {
        for (int o = 0; o < m.columnCount(); o++)
        {
            std::cout << m.getValue(i, o) << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl;
}

int main()
{
    Matrix m(3, 3);

    int value;

    std::cout << "Enter matrix el`s: ";
    for (int r = 0; r < m.rowCount(); r++)
    {
        for (int c = 0; c < m.columnCount(); c++)
        {
            std::cin >> value;

            m.setValue(r, c, value);
        }
    }

    Matrix m1 = m;

    std::cout << "Copied matrix with el`s -100 each: ";
    for (int r = 0; r < m.rowCount(); r++)
    {
        for (int c = 0; c < m.columnCount(); c++)
        {
            m.setValue(r, c, m.getValue(r, c)-100);
        }
    }

    print(m);

    return 0;
}