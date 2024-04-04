with open("input_task3.txt", "r", encoding="utf-8") as file:
    children_data = file.readlines()

children = []
for line in children_data:
    surname, name, age = line.strip().split()
    children.append({"Фамилия": surname, "Имя": name, "возраст": int(age)})

youngest_child = min(children, key=lambda x: x["возраст"])
oldest_child = max(children, key=lambda x: x["возраст"])

with open("output_task3_old.txt", "w",encoding="utf-8") as file:
    file.write(f"Фамилия: {oldest_child['Фамилия']}\n")
    file.write(f"Имя: {oldest_child['Имя']}\n")
    file.write(f"Возраст: {oldest_child['возраст']}\n")

with open("output_task3._young.txt", "w",encoding="utf-8") as file:
    file.write(f"Фамилия: {youngest_child['Фамилия']}\n")
    file.write(f"Имя: {youngest_child['Имя']}\n")
    file.write(f"Возраст: {youngest_child['возраст']}\n")