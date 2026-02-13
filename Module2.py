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
        title = QLabel('Теория: Словари в Python')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Текст теории
        theory_text = QTextEdit()
        theory_text.setReadOnly(True)
        theory_text.setFont(QFont('Arial', 12))
        
        theory_content = """
        <h2>Словари (dict) в Python</h2>
        
        <h3>1. Что такое словарь?</h3>
        <p>Словарь (dict) - это изменяемая коллекция пар "ключ-значение". 
        Ключи должны быть уникальными и неизменяемыми (строки, числа, кортежи).</p>
        
        <h3>2. Создание словаря</h3>
        <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 5px;">
        # Пустой словарь
        d1 = {}
        d2 = dict()
        
        # Словарь с элементами
        student = {'name': 'Иван', 'age': 20, 'course': 'Python'}
        
        # Использование dict()
        colors = dict(red='красный', blue='синий')
        </pre>
        
        <h3>3. Основные операции</h3>
        <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 5px;">
        # Доступ к элементу
        print(student['name'])  # Иван
        
        # Добавление/изменение элемента
        student['grade'] = 'A'
        student['age'] = 21
        
        # Удаление элемента
        del student['course']
        
        # Проверка наличия ключа
        if 'name' in student:
            print('Ключ существует')
        </pre>
        
        <h3>4. Методы словарей</h3>
        <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 5px;">
        student = {'name': 'Иван', 'age': 20}
        
        # get() - получение значения
        age = student.get('age')  # 20
        phone = student.get('phone', 'нет')  # 'нет'
        
        # keys() - все ключи
        keys = student.keys()  # dict_keys(['name', 'age'])
        
        # values() - все значения
        values = student.values()  # dict_values(['Иван', 20])
        
        # items() - пары ключ-значение
        for key, value in student.items():
            print(f'{key}: {value}')
        
        # update() - объединение словарей
        student.update({'city': 'Москва', 'age': 21})
        
        # pop() - удаление с возвратом значения
        name = student.pop('name')
        </pre>
        
        <h3>5. Особенности</h3>
        <ul>
        <li>Словари не сохраняют порядок в версиях Python до 3.7</li>
        <li>Быстрый доступ к элементам по ключу: O(1)</li>
        <li>Ключи должны быть хешируемыми</li>
        <li>Значения могут быть любого типа</li>
        </ul>
        
        <h3>6. Генераторы словарей</h3>
        <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 5px;">
        # Создание словаря квадратов чисел
        squares = {x: x*x for x in range(1, 6)}
        # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
        
        # Фильтрация словаря
        numbers = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        even = {k: v for k, v in numbers.items() if v % 2 == 0}
        </pre>
        
        <h3>7. Вложенные словари</h3>
        <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 5px;">
        # Создание вложенного словаря
        students = {
            'ivan': {'age': 20, 'grade': 'A'},
            'maria': {'age': 21, 'grade': 'B'}
        }
        
        # Доступ к вложенным данным
        print(students['ivan']['age'])  # 20
        </pre>
        
        <h3>8. Полезные функции</h3>
        <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 5px;">
        # len() - количество элементов
        print(len(student))  # 2
        
        # in - проверка наличия ключа
        print('age' in student)  # True
        
        # clear() - очистка словаря
        student.clear()
        
        # copy() - поверхностная копия
        student_copy = student.copy()
        </pre>
        """
        
        theory_text.setHtml(theory_content)
        layout.addWidget(theory_text)
        
        # Кнопка возврата
        back_btn = QPushButton('Назад')
        back_btn.clicked.connect(self.close)
        layout.addWidget(back_btn)
        
        self.setLayout(layout)