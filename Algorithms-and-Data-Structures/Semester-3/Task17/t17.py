class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def parse_tree(s):
    def parse_subtree(start):
        value = ''
        while start < len(s) and (s[start].isdigit() or s[start] == '-'):
            value += s[start]
            start += 1

        if not value:
            return None, start

        node = Node(int(value))

        if start < len(s) and s[start] == '(':
            start += 1
            node.left, start = parse_subtree(start)
            if start < len(s) and s[start] == ',':
                start += 1
                node.right, start = parse_subtree(start)
            if start < len(s) and s[start] == ')':
                start += 1

        return node, start

    tree, _ = parse_subtree(0)
    return tree


def tree_to_string(node):
    if node is None:
        return ''

    left = tree_to_string(node.left)
    right = tree_to_string(node.right)

    if left or right:
        return f'{node.value}({left},{right})'
    else:
        return f'{node.value}'


def search(root, key):
    if root is None or root.value == key:
        return root

    if key < root.value:
        return search(root.left, key)
    else:
        return search(root.right, key)


def insert(root, key):
    if root is None:
        return Node(key)

    if key < root.value:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)

    return root


def delete(root, key):
    if root is None:
        return root

    if key < root.value:
        root.left = delete(root.left, key)
    elif key > root.value:
        root.right = delete(root.right, key)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left

        min_node = find_min(root.right)
        root.value = min_node.value
        root.right = delete(root.right, min_node.value)

    return root


def find_min(node):
    current = node
    while current.left is not None:
        current = current.left
    return current


def menu():
    print("\n1. Поиск вершины")
    print("2. Добавление вершины")
    print("3. Удаление вершины")
    print("4. Выход")


def main():
    tree_string = '8(3(1,6(4,7)),10(,14(13,)))'

    root = parse_tree(tree_string)

    while True:
        menu()
        choice = input("Выберите операцию: ")

        if choice == '1':
            key = int(input("Введите ключ для поиска: "))
            result = search(root, key)
            if result:
                print(f"Вершина {key} найдена.")
            else:
                print(f"Вершина {key} не найдена.")

        elif choice == '2':
            key = int(input("Введите ключ для добавления: "))
            root = insert(root, key)
            print(f"Вершина {key} добавлена.")

        elif choice == '3':
            key = int(input("Введите ключ для удаления: "))
            root = delete(root, key)
            print(f"Вершина {key} удалена.")

        elif choice == '4':
            print("\nВыход. Дерево в линейно-скобочной записи:")
            print(tree_to_string(root))
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == '__main__':
    main()
