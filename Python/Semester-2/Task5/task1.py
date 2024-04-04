with open("input_task1.txt", "r") as file:
    numbers = file.readline().split()
    numbers = [int(num) for num in numbers]

    product = 1
    for num in numbers:
        product *= num


with open("output_task1.txt", "w") as file:
    file.write(str(product))
