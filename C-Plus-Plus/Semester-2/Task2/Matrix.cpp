#include "Matrix.hpp"
#include <iostream>

Matrix::Matrix(int row, int column)
{
    ROW = row;
    COLUMN = column;
    MATRIX = new int* [row];

    for (int i = 0; i < row; i++)
    {
        MATRIX[i] = new int[column];
    }
}

Matrix::Matrix(const Matrix& other) : Matrix::Matrix(other.ROW, other.COLUMN)
{
    for (int row = 0; row < ROW; row++)
    {
        for (int col = 0; col < COLUMN; col++)
        {
            MATRIX[row][col] = other.getValue(row, col);
        }
    }
}

Matrix& Matrix::operator =(Matrix other)
{
    swap(other);
    return *this;
}

Matrix::~Matrix()
{
    for (int i = 0; i < ROW; i++)
        delete[] MATRIX[i];
    delete[] MATRIX;
}

int Matrix::rowCount() const
{
    return ROW;
}

int Matrix::columnCount() const
{
    return COLUMN;
}

int Matrix::getValue(int row, int column) const
{
    return MATRIX[row][column];
}

void Matrix::setValue(int row, int column, int value)
{
    MATRIX[row][column] = value;
}

void Matrix::swap(Matrix& other)
{
    std::swap(ROW, other.ROW);
    std::swap(COLUMN, other.COLUMN);
    std::swap(MATRIX, other.MATRIX);
}