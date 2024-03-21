def check_city(city, cities):
    if city in cities:
        return True
    else:
        cities.add(city)
        return False


def main():
    cities = set()
    while True:
        city = input("Введите название города (или 'стоп', чтобы завершить игру): ").strip().capitalize()
        if city == 'Стоп':
            print("Игра завершена.")
            break
        elif check_city(city, cities):
            print("Этот город уже был назван.")
        else:
            print("Город принят.")


if __name__ == "__main__":
    main()
