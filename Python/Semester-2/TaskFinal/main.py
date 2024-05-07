import csv
import os
import random


def WriteData(learning, testing):
    with open('workdata/learning/train.csv', mode='w') as file:
        output = [','.join(row) for row in learning]

        for i in range(len(output)):
            file.write(f"{output[i]}\n")

    with open('workdata/testing/test.csv', mode='w') as file:
        output = [','.join(row) for row in testing]

        for i in range(len(output)):
            file.write(f"{output[i]}\n")


class CSVReader:
    data = list()

    def __init__(self, filename):
        with open(filename, 'r') as document:
            file = csv.reader(document)
            for line in file:
                self.data.append(line)

    def Show(self, typeOut="top", count=5, separator=','):
        _iter = (self.data[n] for n in range(1, len(self.data)))
        if typeOut == 'bottom':
            _iter = (self.data[n] for n in range(len(self.data) - 1, 0, -1))
        if typeOut == 'random':
            _iter = (i for i in random.sample(self.data[1:], count))

        print(' '.join(self.data[0]))

        for row in range(count):
            print(separator.join(next(_iter)))

    def Info(self):
        row = len(self.data) - 1
        column = len(self.data[0])
        _max = max([len(field) for field in self.data[0]])

        print(f'{row}x{column}')

        for field in range(column):
            non_empty = sum(1 for i in self.data[1:] if i[field])
            field_type = type(self.data[1][field]).__name__

            print(f'{self.data[0][field] + ' ' * (_max - len(self.data[0][field]))}\t{non_empty}\t{field_type}')

    def DelNan(self):
        self.data = [row for row in self.data if all(row)]

    def MakeDS(self):
        learning = random.sample(self.data[1:], int(0.7 * (len(self.data) - 1)))
        testing = [row for row in self.data[1:] if row not in learning]

        os.makedirs('workdata/learning', exist_ok=True)
        os.makedirs('workdata/testing', exist_ok=True)

        WriteData(learning, testing)


def run():
    r = CSVReader("Titanic.csv")
    r.Show()
    r.Show(typeOut="bottom")
    r.Show(typeOut="random")
    r.Info()
    r.DelNan()
    r.Info()
    r.MakeDS()


if __name__ == '__main__':
    run()
