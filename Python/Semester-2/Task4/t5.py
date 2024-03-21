def count_units(n):
    purchases = {}
    for _ in range(n):
        entry = input("Введите запись о покупке (ID Покупателя Товар Количество): ").split()
        buyer_id, item, quantity = entry[0], entry[1], int(entry[2])
        if buyer_id not in purchases:
            purchases[buyer_id] = []
        purchases[buyer_id].append((item, quantity))
    return purchases


def main():
    n = int(input("Введите количество записей о покупках: "))
    purchases = count_units(n)
    for buyer_id, items in purchases.items():
        print(f"Покупатель с ID {buyer_id}:")
        for item, quantity in items:
            print(f"- Товар: {item}, Количество: {quantity}")


if __name__ == "__main__":
    main()
