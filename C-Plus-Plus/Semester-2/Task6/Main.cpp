#include <iostream>
#include <utility>

template<typename T>
class Vector {};

template<>
class Vector<bool> {
    char *_array;
    size_t _size;

    size_t _bits_count;


/**
 * Этот метод создает массив _array заданного размера size,
 * используя оператор new. Он инициализирует каждый элемент массива значением по умолчанию,
 * равным 0. Это необходимо, чтобы убедиться, что все биты в массиве
 * устанавливаются в начальное значение (в данном случае - 0).
 **/
    void createArray(size_t size) {
        _array = new char[size]();
    }

    /**
     * Этот метод создает копию массива _array и возвращает указатель на эту копию.
     * Он используется, когда необходимо создать копию массива для временного хранения
     * его содержимого, например, при расширении массива.
     */
    char *copyArray() {
        auto copy = new char[_size]();
        std::copy(_array, _array + _size, copy);
        return copy;
    }

    /**
     * Этот метод копирует содержимое массива array указанного размера size
     * в массив _array. Он используется для копирования содержимого другого массива в текущий массив.
     */
    void copyToArray(char *array, size_t size) {
        std::copy(array, array + size, _array);
    }

    /**
     * Этот метод увеличивает размер массива _array на один элемент.
     * Для этого он создает временную копию текущего массива, удаляет текущий массив,
     * выделяет новый массив с увеличенным размером,
     * копирует содержимое временной копии в новый массив и затем освобождает память, выделенную под временную копию.
     */
    void expandArray() {
        auto new_size = _size + 1;

        auto temp_copy = copyArray();
        deleteArray();
        createArray(new_size);
        copyToArray(temp_copy, _size);
        delete[] temp_copy;

        _size = new_size;
    }

    void deleteArray() {
        delete[] _array;
    }

public:
    /**
     * Этот конструктор принимает количество битов (bits_count)
     * и инициализирует объект класса Vector<bool>.
     * Первым делом он проверяет, что количество битов не равно нулю,
     * потому что вектор с нулевым размером не имеет смысла.
     * Затем вычисляется размер массива _array в байтах, необходимый для хранения заданного количества битов.
     * Для этого используется формула: _size = (bits_count - 1) / 8 + 1, которая учитывает,
     * что каждое значение булевского типа занимает 1 бит, и округляет количество битов
     * до целого количества байтов, необходимых для хранения их.
     * После вычисления размера массива вызывается метод createArray(_size),
     * который выделяет память под массив _array заданного размера.
     */
    explicit Vector(size_t bits_count) { // NOLINT(cppcoreguidelines-pro-type-member-init)
        if (bits_count == 0) {
            std::cerr << "Invalid bits count" << std::endl;
            exit(1);
        }

        _bits_count = bits_count;

        _size = (bits_count - 1) / 8 + 1;
        createArray(_size);
    }

    ~Vector() {
        deleteArray();
    }

    Vector(const Vector &other) : Vector(other._bits_count) {  // NOLINT(cppcoreguidelines-pro-type-member-init)
        copyToArray(other._array, other._size);
    }

    Vector &operator=(const Vector &other) {
        if (this == &other) return *this;

        _size = other._size;

        deleteArray();
        createArray(_size);
        copyToArray(other._array, other._size);
    }

    bool operator[](size_t index) {
        return get(index);
    }

    size_t size() const {
        return _bits_count;
    }

    bool get(size_t index) {
        auto position = std::make_pair((index) / 8, index % 8);

        return (_array[position.first] >> (8 - 1 - position.second)) & 1;
    }

    /**
     * Этот метод устанавливает значение бита по указанному индексу в векторе.
     * Сначала вычисляется позиция бита в массиве _array с помощью метода calculatePosition(index).
     * Затем происходит установка значения бита в массиве _array в соответствии с переданным значением.
     */
    void set(size_t index, bool value) {
        auto position = std::make_pair((index) / 8, index % 8);

        if (value)
            _array[position.first] = _array[position.first] | (1 << (8 - 1 - position.second));
        else
            _array[position.first] = _array[position.first] & ~(1 << (8 - 1 - position.second));
    }

    void pushBack(bool value) {
        if (_bits_count % 8 == 0) {
            expandArray();
        }
        set(_bits_count, value);

        _bits_count++;
    }

    /**
     * Этот метод вставляет новый бит в вектор по указанному индексу.
     * Если количество битов кратно 8, вызывается метод expandArray(), чтобы увеличить размер массива _array.
     * Затем все биты после указанного индекса сдвигаются на одну позицию вправо,
     * чтобы освободить место для нового бита, и новое значение устанавливается по указанному индексу.
     */
    void insert(size_t index, bool value) {
        if (_bits_count % 8 == 0) {
            expandArray();
        }
        _bits_count++;

        for (auto last_index = _bits_count - 1; last_index > index; last_index--) {
            set(last_index, get(last_index - 1));
        }
        set(index, value);
    }

    void erase(size_t index) {
        _bits_count--;

        for (auto first_index = index; first_index < _bits_count; first_index++) {
            set(first_index, get(first_index + 1));
        }
        set(_bits_count, false);
    }

    void print() {
        for (size_t i = 0; i < size(); i++) {
            std::cout << (*this)[i];
        }
        std::cout << std::endl;
    }
};


int main() {
    Vector<bool> v(4);

    v.set(0, true);  //1
    v.set(1, true);  //1
    v.set(2, false); //0
    v.set(3, false); //0
    v.pushBack(false);    //0
    v.pushBack(true);     //1

    std::cout << std::endl;
    std::cout << "Vector size is: " << v.size() << std::endl;
    std::cout << "Vector is: ";
    v.print();

    std::cout << std::endl;
    std::cout << "Inserting some values.." << std::endl;
    v.insert(7, false);
    v.insert(7, true);

    std::cout << "Vector size is: " << v.size() << std::endl;
    std::cout << "Vector is: ";
    v.print();

    std::cout << std::endl;
    std::cout << "Erasing some values.." << std::endl;
    v.erase(0);
    v.erase(0);

    std::cout << "Vector size is: " << v.size() << std::endl;
    std::cout << "Vector is: ";
    v.print();

    return 0;
}