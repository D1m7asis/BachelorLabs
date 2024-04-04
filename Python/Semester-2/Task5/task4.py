import json
import csv
import os
import sys


def json_to_csv(file):
    csv_filename = os.path.splitext(file)[0] + '.csv'
    with open(file, 'r') as f:
        data = json.load(f)

        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            if isinstance(data, list):
                headers = list(data[0].keys())
                writer.writerow(headers)

                for item in data:
                    writer.writerow(item.values())
            else:
                headers = list(data.keys())
                writer.writerow(headers)
                writer.writerow(data.values())

    print(f"CSV файл успешно создан: {csv_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Пример использования: python json2csv.py example.json")
        sys.exit(1)

    json_f = sys.argv[1]

    if not os.path.exists(json_f):
        print(f"{json_f} не найден.")
        sys.exit(1)

    json_to_csv(json_f)
