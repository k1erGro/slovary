import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class TheoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Теория - Словари Python')
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        # Заголовок
        title = QLabel('📚 Теория: Словари в Python')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Создаём вкладки
        tabs = QTabWidget()
        tabs.setFont(QFont('Arial', 10))

        # Вкладка 1: Введение
        intro_tab = self.create_tab("""
            <h2>Что такое словарь?</h2>
            <p>Словарь (dict) в Python — это неупорядоченная коллекция произвольных объектов с доступом по ключу. 
            Их иногда называют ассоциативными массивами или хеш-таблицами.</p>

            <h3>Основные характеристики:</h3>
            <ul>
                <li>Изменяемый (можно добавлять, удалять, изменять элементы)</li>
                <li>Неупорядоченный (до версии 3.7 порядок не гарантировался)</li>
                <li>Ключи должны быть уникальными и неизменяемыми (строки, числа, кортежи)</li>
                <li>Значения могут быть любого типа</li>
            </ul>

            <h3>Создание словаря:</h3>
            <pre>
# Пустой словарь
d1 = {}
d2 = dict()

# Словарь с элементами
student = {'name': 'Иван', 'age': 20, 'course': 'Python'}

# Использование dict()
colors = dict(red='красный', blue='синий')
            </pre>
        """)
        tabs.addTab(intro_tab, "Введение")

        # Вкладка 2: Основные операции
        operations_tab = self.create_tab("""
            <h2>Основные операции со словарями</h2>

            <h3>Доступ к элементам:</h3>
            <pre>
student = {'name': 'Иван', 'age': 20}
print(student['name'])      # Иван
print(student.get('age'))    # 20
print(student.get('phone', 'Нет телефона'))  # 'Нет телефона'
            </pre>

            <h3>Добавление и изменение:</h3>
            <pre>
student['grade'] = 'A'      # добавление нового ключа
student['age'] = 21          # изменение существующего
            </pre>

            <h3>Удаление:</h3>
            <pre>
del student['course']        # удаление ключа
age = student.pop('age')      # удаление с возвратом значения
student.clear()               # очистка всего словаря
            </pre>

            <h3>Проверка наличия ключа:</h3>
            <pre>
if 'name' in student:
    print('Ключ существует')
            </pre>
        """)
        tabs.addTab(operations_tab, "Операции")

        # Вкладка 3: Методы
        methods_tab = self.create_tab("""
            <h2>Методы словарей</h2>

            <pre>
student = {'name': 'Иван', 'age': 20, 'city': 'Москва'}

# keys() - все ключи
print(student.keys())   # dict_keys(['name', 'age', 'city'])

# values() - все значения
print(student.values()) # dict_values(['Иван', 20, 'Москва'])

# items() - пары ключ-значение
for key, value in student.items():
    print(f'{key}: {value}')

# update() - обновление/объединение словарей
student.update({'course': 'Python', 'age': 21})

# setdefault() - получить значение, если ключ есть, иначе создать с default
city = student.setdefault('city', 'Неизвестно')

# copy() - поверхностная копия
student_copy = student.copy()
            </pre>
        """)
        tabs.addTab(methods_tab, "Методы")

        # Вкладка 4: Генераторы и особенности
        advanced_tab = self.create_tab("""
            <h2>Генераторы словарей и особенности</h2>

            <h3>Генераторы словарей (dict comprehensions):</h3>
            <pre>
# Создание словаря квадратов чисел
squares = {x: x*x for x in range(1, 6)}
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Фильтрация словаря
numbers = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
even = {k: v for k, v in numbers.items() if v % 2 == 0}
# {'b': 2, 'd': 4}
            </pre>

            <h3>Вложенные словари:</h3>
            <pre>
# Словарь словарей
students = {
    'ivan': {'age': 20, 'grade': 'A'},
    'maria': {'age': 21, 'grade': 'B'}
}
print(students['ivan']['age'])  # 20
            </pre>

            <h3>Полезные функции:</h3>
            <pre>
# len() - количество элементов
print(len(student))  # 3

# sorted() - сортировка ключей
for key in sorted(student):
    print(key, student[key])
            </pre>
        """)
        tabs.addTab(advanced_tab, "Дополнительно")

        # Вкладка 5: Примеры
        examples_tab = self.create_tab("""
            <h2>Примеры использования словарей</h2>

            <h3>Подсчет частоты слов:</h3>
            <pre>
text = "hello world hello python world"
words = text.split()
freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1
print(freq)  # {'hello': 2, 'world': 2, 'python': 1}
            </pre>

            <h3>Группировка данных:</h3>
            <pre>
persons = [
    ('Иван', 20, 'Москва'),
    ('Мария', 21, 'Москва'),
    ('Петр', 22, 'СПб')
]
cities = {}
for name, age, city in persons:
    cities.setdefault(city, []).append((name, age))
print(cities)
# {'Москва': [('Иван', 20), ('Мария', 21)], 'СПб': [('Петр', 22)]}
            </pre>

            <h3>Кэширование результатов:</h3>
            <pre>
cache = {}
def fibonacci(n):
    if n in cache:
        return cache[n]
    if n < 2:
        result = n
    else:
        result = fibonacci(n-1) + fibonacci(n-2)
    cache[n] = result
    return result
            </pre>
        """)
        tabs.addTab(examples_tab, "Примеры")

        layout.addWidget(tabs)

        # Кнопка возврата
        back_btn = QPushButton('← Назад')
        back_btn.setStyleSheet('background-color: #95a5a6; color: white; padding: 8px;')
        back_btn.clicked.connect(self.close)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def create_tab(self, html_content):
        """Создаёт виджет вкладки с QTextEdit, отображающим HTML."""
        tab = QWidget()
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setFont(QFont('Arial', 11))

        # Оборачиваем контент в базовый HTML со стилями
        full_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial; font-size: 11pt; margin: 10px; }}
                pre {{ background-color: #f4f4f4; padding: 8px; border-radius: 4px; }}
                h2 {{ color: #2c3e50; }}
                h3 {{ color: #3498db; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        text_edit.setHtml(full_html)
        layout.addWidget(text_edit)
        tab.setLayout(layout)
        return tab


# Для автономного тестирования модуля
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TheoryWindow()
    window.show()
    sys.exit(app.exec_())