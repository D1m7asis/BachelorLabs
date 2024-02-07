#ifndef MAIN_RECTANGPP_H
#define MAIN_RECTANGPP_H


class RectangPP {
    double length;
    double width;
    double height;

public:
    RectangPP(double length, double width, double height);

    virtual ~RectangPP();

    double getLength() const;

    void setLength(double newLength);

    double getWidth() const;

    void setWidth(double newWidth);

    double getHeight() const;

    void setHeight(double newHeight);

    double volume() const;

    double totalSurfaceArea() const;

    double diagLength() const;

    double sideSurfaceArea() const;
};

#endif //MAIN_RECTANGPP_H