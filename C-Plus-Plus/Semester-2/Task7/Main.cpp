#include <iostream>
#include <fstream>
#include <memory>
#include <filesystem>

namespace fs = std::filesystem;

class DataReader
{
protected:
    std::ifstream m_in;
    std::string m_filename;
    uint8_t* m_data;
    uint8_t m_n;

public:
    explicit DataReader(const std::string& filename) : m_filename(filename), m_n(0), m_data(nullptr){}
    virtual ~DataReader() = default;
    virtual bool Open() = 0;
    virtual void Read() = 0;
    virtual void GetData(uint8_t* buf, uint8_t& n) = 0;
    void Close(){
        m_in.close();
    }
};

class TxtReader : public DataReader
{
public:
    explicit TxtReader(const std::string& filename) : DataReader(filename) {}
    ~TxtReader() override{
            delete[] m_data;  // Смысла на nullptr проверять нет -- к этому мы и идем
    }
    bool Open() override{
        m_in.open(m_filename);
        return m_in.is_open();
    }
    void Read() override {
        int tmp;
        m_in >> tmp;
        m_n = tmp;
        m_data = new uint8_t[m_n];
        for (int i = 0; i < m_n; i++)
        {
            int loop_tmp;
            m_in >> loop_tmp;
            m_data[i] = loop_tmp;
        }
    }
    void GetData(uint8_t* buf, uint8_t& n) override {}
};

class BinReader : public DataReader
{
public:
    explicit BinReader(const std::string& filename) : DataReader(filename) {}
    ~BinReader() override{
            delete[] m_data;
    }
    bool Open() override{
        m_in.open(m_filename, std::ios::binary);
        if (!m_in.is_open())
            return false;
        return true;
    }
    void Read() override{
        m_in.read((char*)&m_n, 1);
        m_data = new uint8_t[m_n];
        m_in.read((char*)m_data, m_n);
    }
    void GetData(uint8_t* buf, uint8_t& n) override {}
};

class BinFReader : public DataReader
{
public:
    explicit BinFReader(const std::string& filename) : DataReader(filename) {}
    ~BinFReader() override {
            delete[] m_data;
    }
    bool Open() override {
        m_in.open(m_filename, std::ios::binary);
        if (!m_in.is_open())
            return false;
        return true;
    }
    void Read() override {
        uint8_t numFloats;
        m_in.read(reinterpret_cast<char*>(&numFloats), sizeof(uint8_t));
        m_n = numFloats;
        delete[] m_data;
        m_data = new uint8_t[m_n * sizeof(float)];
        m_in.read(reinterpret_cast<char*>(m_data), m_n * sizeof(float));
    }
    void GetData(uint8_t* buf, uint8_t& n) override {
        std::cout << "Number: " << int(m_n) << std::endl;
        for (size_t i = 0; i < m_n*4; i+=4){
            std::cout << *(float*)(m_data+i) << std::endl;
        }
    }
};

std::unique_ptr<DataReader> Factory(const std::string& filename)
{
    std::string extension = filename.substr(filename.find_last_of('.') + 1);

    if (extension == "txt")
        return std::make_unique<TxtReader>(filename);
    else if (extension == "bin")
        return std::make_unique<BinReader>(filename);
    else if (extension == "binf")
        return std::make_unique<BinFReader>(filename);
    return nullptr;
}

void create_bin_file() {
    std::ofstream out("bin_example.bin", std::ios::binary);
    uint8_t buf[6];
    buf[0] = 5;
    for (int i = 0; i < 5; i++)
    {
        buf[i + 1] = i + 127;
    }
    out.write(reinterpret_cast<char*>(buf), 6);

    if (out.is_open()) {
        std::cout << "File created successfully" << std::endl;
        std::cout << "File path: " << fs::absolute("bin_example.bin") << std::endl;
    }
    else {
        std::cerr << "Failed to create file" << std::endl;
    }
}

void create_binf_file() {
    std::ofstream out("binf_example.binf", std::ios::binary);
    float buf[4] = {3.0f, 3.14f, 2.718f, 1.618f};
    uint8_t size = 4;
    out.write(reinterpret_cast<char*>(&size), sizeof(uint8_t));
    out.write(reinterpret_cast<char*>(buf), sizeof(buf));
    if (out.is_open()) {
        std::cout << "File created successfully" << std::endl;
        std::cout << "File path: " << fs::absolute("binf_example.binf") << std::endl;
    }
    else {
        std::cerr << "Failed to create file" << std::endl;
    }
}

int main() {
    create_binf_file();

    uint8_t count = 0;
    uint8_t buf[100];

    std::unique_ptr<DataReader> Reader = Factory("example.binf");

    if (!Reader)
        return -1;
    if (!Reader->Open())
        return -10;

    Reader->Read();
    Reader->GetData(buf, count);
    Reader->Close();

    return 0;
}