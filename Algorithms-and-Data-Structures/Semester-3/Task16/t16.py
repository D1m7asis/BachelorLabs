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


# Нерекурсивный прямой обход (Pre-order) с использованием стека
def iterative_preorder_traversal(root):
    if root is None:
        return ""

    stack = [root]
    result = []

    while stack:
        node = stack.pop()
        result.append(str(node.value))

        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return " ".join(result)


def main():
    tree_string = '8(3(1,6(4,7)),10(,14(13,)))'

    root = parse_tree(tree_string)

    traversal_result = iterative_preorder_traversal(root)
    print("Нерекурсивный прямой обход (Pre-order):")
    print(traversal_result)


if __name__ == '__main__':
    main()
