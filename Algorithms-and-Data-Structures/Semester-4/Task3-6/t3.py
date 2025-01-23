class AhoCorasick:
    # Структура данных автомата

    def __init__(self):
        self.states = 1  # Начальное количество состояний (0 - начальное состояние)
        self.edges = {0: {}}  # Словарь переходов между состояниями
        self.fail = [0]  # Функция перехода при неудаче (fail function)
        self.output = [set()]  # Множество слов, которые заканчиваются в данном состоянии

    def add_word(self, word):
        current_state = 0  # Начинаем с начального состояния

        for char in word:
            if char not in self.edges[current_state]:
                # Если перехода по символу нет, создаем новое состояние
                self.edges[current_state][char] = self.states
                self.edges[self.states] = {}

                self.fail.append(0)  # Инициализируем fail функцию для нового состояния
                self.output.append(set())  # Инициализируем множество слов для нового состояния

                self.states += 1  # Увеличиваем количество состояний

            current_state = self.edges[current_state][char]

        # Добавляем слово в выходное множество текущего состояния
        self.output[current_state].add(word)

    def build_automaton(self):
        from collections import deque

        queue = deque()

        # Инициализируем fail функцию для всех дочерних узлов начального состояния
        for char, state in self.edges[0].items():
            if state != 0:
                self.fail[state] = 0
                queue.append(state)

        # Обрабатываем очередь состояний для построения fail функции
        while queue:
            r = queue.popleft()  # Берем вершину из очереди

            for char, state in self.edges[r].items():
                queue.append(state)  # Добавляем дочерние вершины в очередь
                s = self.fail[r]  # Начинаем поиск fail функции с родительского состояния

                while s != 0 and char not in self.edges[s]:
                    s = self.fail[s]  # Переходим по fail функции до тех пор, пока не найдем подходящий символ

                self.fail[state] = self.edges[s].get(char, 0)  # Определяем fail функцию для текущего состояния

                self.output[state] |= self.output[self.fail[state]]  # Обновляем множество слов для текущего состояния

    def search(self, text):
        results = []  # Список для хранения результатов поиска
        current_state = 0  # Начинаем с начального состояния

        for i, char in enumerate(text):
            # Переходим по символам текста, обновляя текущее состояние
            while current_state != 0 and char not in self.edges[current_state]:
                current_state = self.fail[current_state]  # Переходим по fail функции при неудаче

            if char in self.edges[current_state]:
                current_state = self.edges[current_state][char]  # Переходим к следующему состоянию

            if self.output[current_state]:
                # Если в текущем состоянии есть слова, добавляем их в результаты
                for match in self.output[current_state]:
                    results.append((i - len(match) + 1, match))

        return results


if __name__ == '__main__':
    patterns = ["he", "she", "his", "hers"]
    text = "ahishers"

    aho_corasick = AhoCorasick()

    for pattern in patterns:
        aho_corasick.add_word(pattern)

    aho_corasick.build_automaton()

    matches = aho_corasick.search(text)

    print("Найденные совпадения:")
    for match in matches:
        print(f"Позиция {match[0]}: {match[1]}")
