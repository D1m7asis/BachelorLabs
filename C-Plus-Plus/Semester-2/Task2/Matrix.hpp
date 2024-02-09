#pragma once

class Matrix
{
    int ROW;
    int COLUMN;
    int** MATRIX;

public:
    Matrix(int row, int column);
    Matrix(const Matrix& other);
    ~Matrix();
    Matrix& operator =(Matrix other);
    [[nodiscard]] int rowCount() const;
    [[nodiscard]] int columnCount() const;
    [[nodiscard]] int getValue(int row, int column) const;
    void setValue(int row, int column, int value);
private:
    void swap(Matrix& other);
};