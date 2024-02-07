#include <iostream>
#include "RectangPP.h"

int main() {
    std::setlocale(LC_ALL, "Russian");

    double l, w, h;

    std::cout << "������� �����, ������ � ������ ������\n";

    std::cin >> l;
    std::cin >> w;
    std::cin >> h;

    RectangPP shape(l, w, h);

    std::cout << shape.getLength() << std::endl;
    std::cout << shape.getWidth() << std::endl;
    std::cout << shape.getHeight() << std::endl;

    std::cout << shape.sideSurfaceArea() << std::endl;
    std::cout << shape.totalSurfaceArea() << std::endl;
    std::cout << shape.volume() << std::endl;
    std::cout << shape.diagLength() << std::endl;
}