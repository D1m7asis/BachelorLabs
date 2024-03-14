#include <iostream>
#include <cmath>


template <typename T, size_t M, size_t N>
class Matrix {
    T** matrix = {};

    void init() {
        matrix = new T*[M];
        for(size_t i = 0; i < M; i++)
        {
            matrix[i] = new T[N]();
        }
    }

    void copyMatrixFrom(T** m)
    {
        for(size_t i = 0; i < M; i++)
        {
            for(size_t j = 0; j < N; j++)
            {
                m[i][j] = m[i][j];
            }
        }
    }

    void del() {

        for(size_t i = 0; i < M; i++)
        {
            delete[] matrix[i];
        }

        delete[] matrix;
    }


public:
    Matrix() {
        init();
    }

    ~Matrix() {
        del();
    }

    Matrix(const Matrix& other) : Matrix() {
        copyMatrixFrom(other.matrix);
    }



    T& operator()(size_t i, size_t j)
    {
        return matrix[i][j];
    }

    Matrix operator+(const Matrix& other) {
        Matrix copy(*this);
        copy += other;

        return copy;
    }

    Matrix& operator=(const Matrix& other) {
        if (this == &other)
        {
            return *this;
        }

        copyMatrixFrom(other.matrix);

        return *this;
    }

    Matrix& operator+=(const Matrix& other) {
        for(size_t i = 0; i < M; i++)
        {
            for(size_t j = 0; j < N; j++)
            {
                matrix[i][j] += other.matrix[i][j];
            }
        }

        return *this;
    }

    Matrix operator*=(T number) {
        for(size_t i = 0; i < M; i++)
        {
            for(size_t j = 0; j < N; j++)
            {
                matrix[i][j] *= number;
            }
        }

        return *this;
    };

    void operator++(int)
    {
        for(size_t i = 0; i < M; i++)
        {
            for(size_t j = 0; j < N; j++)
            {
                matrix[i][j]++;
            }
        }
    }

    template <size_t H>
    Matrix<T, M, H> operator*(Matrix<T, N, H>& other) {
        Matrix<T, M, H> new_matrix;

        for(size_t k = 0; k < H; k++)
        {
            for(size_t i = 0; i < M; i++)
            {
                T item{};

                for(size_t j = 0; j < N; j++)
                {
                    item += matrix[i][j] * other(j, k);
                }

                new_matrix(i, k) = item;
            }
        }

        return new_matrix;
    }



    long det() {
        if ((M != N) | (M > 3))
        {
            std::cerr << "User Input Err" << std::endl;
            exit(1);
        }

        switch (M)
        {
            case 1:
                return matrix[0][0];
            case 2:
                return matrix[0][0] * matrix[1][1] - (matrix[0][1] * matrix[1][0]);
            default:
                return (
                        (matrix[0][0] * matrix[1][1] * matrix[2][2])
                      - (matrix[0][0] * matrix[1][2] * matrix[2][1])
                      - (matrix[0][1] * matrix[1][0] * matrix[2][2])
                      + (matrix[0][1] * matrix[1][2] * matrix[2][0])
                      + (matrix[0][2] * matrix[1][0] * matrix[2][1])
                      - (matrix[0][2] * matrix[1][1] * matrix[2][0])
                );
        }
    }

    void randomize() {

        for (size_t i = 0; i < M; i++)
        {
            for (size_t j = 0; j < N; j++)
            {
                matrix[i][j] = ((rand() % 10) + 1);
            }
        }
    }
};


template <typename T, size_t M, size_t N>
std::ostream& operator<<(std::ostream& out, Matrix<T, M, N>& matrix) {
    for(size_t i = 0; i < M; i++)
    {
        for(size_t j = 0; j < N; j++)
        {
            out << matrix(i, j) << " ";
        }

        if (i != M-1) out << std::endl;
    }
    return out;
}


template <typename T, size_t M, size_t N>
std::istream& operator>>(std::istream& in, Matrix<T, M, N>& matrix) {
    for(size_t i = 0; i < M; i++)
    {
        for(size_t j = 0; j < N; j++)
        {
            std::cin >> matrix(i, j);
        }
    }

    return in;
}

void printDebugInfo() {
    Matrix<int, 2, 3> A{};
    Matrix<int, 3, 3> B{};

    A.randomize();
    B.randomize();

    std::cout << "A" << std::endl <<  A << std::endl << std::endl;
    std::cout << "B" << std::endl <<  B << std::endl << std::endl;


    std::cout << "A * B" << std::endl;
    Matrix<int, 2, 3> A_B = A * B;
    std::cout << A_B << std::endl << std::endl;

    std::cout << "Det B" << std::endl;
    std::cout << B.det() << std::endl << std::endl;

    std::cout << "A + (A +B)" << std::endl;
    A += A_B;
    std::cout << A << std::endl << std::endl;

    std::cout << "A++" << std::endl;
    A++;
    std::cout << A << std::endl << std::endl;
    std::cout << "A * 2" << std::endl;
    A *= 2;
    std::cout << A << std::endl << std::endl;

    std::cout << "Set `n` get" << std::endl;
    A(0, 0) = 0;
    std::cout << A(0, 0) << " " << A(1, 0) << std::endl;

}


int main() {
    printDebugInfo();

    return 0;
}