#include "RectangPP.h"
#include <cmath>
#include <iostream>

double length;
double width;
double height;

RectangPP::RectangPP(double c_length, double c_width, double c_height) {
    length = c_length;
    width = c_width;
    height = c_height;

    std::cout << "Shape with dim`s " << length << " " << width << " " << height << " was created.\n";
}

double RectangPP::getLength() const {
    return length;
}

void RectangPP::setLength(double newLength) {
    RectangPP::length = newLength;
}

double RectangPP::getWidth() const {
    return width;
}

void RectangPP::setWidth(double newWidth) {
    RectangPP::width = newWidth;
}

double RectangPP::getHeight() const {
    return height;
}

void RectangPP::setHeight(double newHeight) {
    RectangPP::height = newHeight;
}

RectangPP::~RectangPP() = default;

double RectangPP::volume() const {
    return length*width*height;
}

double RectangPP::totalSurfaceArea() const {
    return 2*(length*width + width*height + height*length);
}

double RectangPP::diagLength() const {
    return sqrt(length*length + width*width + height*height);
}

double RectangPP::sideSurfaceArea() const {
    return 2*(width+length)*height;
}