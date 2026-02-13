import json
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class TestWindow(QWidget):
    def __init__(self, username, users):
        super().__init__()
        self.username = username
        self.users = users
        self.current_question = 0
        self.score = 0
        self.answers = []
        self.questions = self.load_questions()
        self.init_ui()

    def load_questions(self):
        return [
            {
                'question': 'Как создать пустой словарь в Python?',
                'options': [
                    '{}',
                    'dict()',
                    '[]',
                    'set()'
                ],
                'correct': [0, 1],
                'type': 'multiple',
                'explanation': 'Пустой словарь можно создать с помощью фигурных скобок {} или функции dict()'
            },
            {
                'question': 'Как получить значение по ключу "name" из словаря person?',
                'options': [
                    'person[name]',
                    'person.get("name")',
                    'person("name")',
                    'person.key("name")'
                ],
                'correct': [0, 1],
                'type': 'multiple',
                'explanation': 'Можно использовать квадратные скобки person[name] или метод get()'
            },
            {
                'question': 'Какой метод возвращает все ключи словаря?',
                'options': [
                    'keys()',
                    'values()',
                    'items()',
                    'all_keys()'
                ],
                'correct': [0],
                'type': 'single',
                'explanation': 'Метод keys() возвращает представление всех ключей словаря'
            },
            {
                'question': 'Что вернет person.get("age", 0) если ключа "age" нет?',
                'options': [
                    '0',
                    'None',
                    'KeyError',
                    'False'
                ],
                'correct': [0],
                'type': 'single',
                'explanation': 'Метод get() возвращает значение по умолчанию (0), если ключ не найден'
            },
            {
                'question': 'Как добавить элемент {"city": "Moscow"} в словарь data?',
                'options': [
                    'data.append({"city": "Moscow"})',
                    'data.update({"city": "Moscow"})',
                    'data["city"] = "Moscow"',
                    'data.add({"city": "Moscow"})'
                ],
                'correct': [1, 2],
                'type': 'multiple',
                'explanation': 'Можно использовать метод update() или присваивание по ключу'
            },
            {
                'question': 'Как удалить элемент с ключом "temp" и получить его значение?',
                'options': [
                    'del data["temp"]',
                    'data.remove("temp")',
                    'data.pop("temp")',
                    'data.delete("temp")'
                ],
                'correct': [2],
                'type': 'single',
                'explanation': 'Метод pop() удаляет элемент и возвращает его значение'
            },
            {
                'question': 'Как перебрать все пары ключ-значение в словаре?',
                'options': [
                    'for key in dict:',
                    'for key, value in dict.items():',
                    'for value in dict.values():',
                    'for item in dict:'
                ],
                'correct': [1],
                'type': 'single',
                'explanation': 'Метод items() возвращает пары (ключ, значение) для итерации'
            },
            {
                'question': 'Какой из этих типов НЕ может быть ключом словаря?',
                'options': [
                    'Строка (str)',
                    'Кортеж (tuple)',
                    'Список (list)',
                    'Число (int)'
                ],
                'correct': [2],
                'type': 'single',
                'explanation': 'Ключом словаря может быть только неизменяемый тип данных'
            },
            {
                'question': 'Что делает метод setdefault()?',
                'options': [
                    'Устанавливает значение по умолчанию для ключа',
                    'Удаляет ключ со значением по умолчанию',
                    'Проверяет наличие ключа',
                    'Изменяет тип ключа'
                ],
                'correct': [0],
                'type': 'single',
                'explanation': 'setdefault(key, default) возвращает значение ключа, если он существует, иначе устанавливает ключ в default'
            },
            {
                'question': 'Как создать копию словаря?',
                'options': [
                    'dict.copy()',
                    'dict.clone()',
                    'dict[:]',
                    'copy(dict)'
                ],
                'correct': [0],
                'type': 'single',
                'explanation': 'Метод copy() создает поверхностную копию словаря'
            }
        ]

    def init_ui(self):
        self.setWindowTitle('Тест по словарям Python')
        self.setFixedSize(700, 550)
        
        layout = QVBoxLayout()
        
        # Верхняя панель с прогрессом
        top_layout = QHBoxLayout()
        
        self.progress = QLabel(f'Вопрос 1 из {len(self.questions)}')
        self.progress.setFont(QFont('Arial', 10, QFont.Bold))
        
        self.score_label = QLabel('Счет: 0')
        self.score_label.setFont(QFont('Arial', 10, QFont.Bold))
        
        top_layout.addWidget(self.progress)
        top_layout.addStretch()
        top_layout.addWidget(self.score_label)
        
        layout.addLayout(top_layout)
        
        # Вопрос
        self.question_label = QLabel()
        self.question_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet('padding: 10px; background-color: #f0f0f0; border-radius: 5px;')
        layout.addWidget(self.question_label)
        
        # Варианты ответов
        self.options_group = QButtonGroup()
        self.options_group.setExclusive(False)
        self.options_widget = QWidget()
        self.options_layout = QVBoxLayout()
        self.options_widget.setLayout(self.options_layout)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.options_widget)
        layout.addWidget(scroll)
        
        # Кнопки навигации
        nav_layout = QHBoxLayout()
        
        self.prev_btn = QPushButton('◀ Назад')
        self.prev_btn.clicked.connect(self.prev_question)
        
        self.next_btn = QPushButton('Далее ▶')
        self.next_btn.clicked.connect(self.next_question)
        
        self.finish_btn = QPushButton('✅ Завершить тест')
        self.finish_btn.clicked.connect(self.finish_test)
        self.finish_btn.setStyleSheet('background-color: #4CAF50; color: white; font-weight: bold;')
        self.finish_btn.hide()
        
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.next_btn)
        nav_layout.addWidget(self.finish_btn)
        
        layout.addLayout(nav_layout)
        
        self.setLayout(layout)
        self.show_question()

    def show_question(self):
        # Очистка предыдущих вариантов
        for i in reversed(range(self.options_layout.count())):
            widget = self.options_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        question = self.questions[self.current_question]
        
        # Обновление прогресса
        self.progress.setText(f'Вопрос {self.current_question + 1} из {len(self.questions)}')
        
        # Отображение вопроса
        self.question_label.setText(f"{self.current_question + 1}. {question['question']}")
        
        # Создание вариантов ответов
        self.option_widgets = []
        for i, option in enumerate(question['options']):
            if question['type'] == 'single':
                rb = QRadioButton(f"{chr(65 + i)}. {option}")  # A, B, C, D
                rb.setFont(QFont('Arial', 11))
                self.options_group.addButton(rb, i)
                self.options_layout.addWidget(rb)
                self.option_widgets.append(rb)
            else:
                cb = QCheckBox(f"{chr(65 + i)}. {option}")
                cb.setFont(QFont('Arial', 11))
                self.options_group.addButton(cb, i)
                self.options_layout.addWidget(cb)
                self.option_widgets.append(cb)
        
        # Восстановление ответа, если он был дан ранее
        if self.current_question < len(self.answers):
            answer = self.answers[self.current_question]
            for i in answer:
                if i < len(self.option_widgets):
                    self.option_widgets[i].setChecked(True)
        
        # Обновление кнопок навигации
        self.prev_btn.setEnabled(self.current_question > 0)
        if self.current_question == len(self.questions) - 1:
            self.next_btn.hide()
            self.finish_btn.show()
        else:
            self.next_btn.show()
            self.finish_btn.hide()

    def save_answer(self):
        answer = []
        for i, widget in enumerate(self.option_widgets):
            if widget.isChecked():
                answer.append(i)
        
        if self.current_question >= len(self.answers):
            self.answers.append(answer)
        else:
            self.answers[self.current_question] = answer

    def prev_question(self):
        self.save_answer()
        self.current_question -= 1
        self.show_question()

    def next_question(self):
        self.save_answer()
        self.current_question += 1
        self.show_question()

    def finish_test(self):
        self.save_answer()
        self.calculate_score()
        self.show_results()

    def calculate_score(self):
        self.score = 0
        self.correct_answers = []
        
        for i, question in enumerate(self.questions):
            if i < len(self.answers):
                user_answer = set(self.answers[i])
                correct_answer = set(question['correct'])
                if user_answer == correct_answer:
                    self.score += 1
                    self.correct_answers.append(True)
                else:
                    self.correct_answers.append(False)
            else:
                self.correct_answers.append(False)
        
        # Сохранение результата
        result = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'score': self.score,
            'total': len(self.questions),
            'percentage': int((self.score / len(self.questions)) * 100),
            'answers': self.answers
        }
        
        self.users[self.username]['tests'].append(result)
        
        # Сохранение в файл
        with open('users.json', 'w') as f:
            json.dump(self.users, f, indent=2)

    def show_results(self):
        result_window = QDialog(self)
        result_window.setWindowTitle('Результаты теста')
        result_window.setFixedSize(500, 600)
        
        layout = QVBoxLayout()
        
        title = QLabel('Результаты теста')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        percentage = int((self.score / len(self.questions)) * 100)
        
        # Отображение результата с иконкой
        result_text = QLabel()
        result_text.setAlignment(Qt.AlignCenter)
        
        if percentage >= 90:
            icon = "🎯"
            grade = "Отлично!"
            color = "#4CAF50"
        elif percentage >= 70:
            icon = "👍"
            grade = "Хорошо!"
            color = "#2196F3"
        elif percentage >= 50:
            icon = "👌"
            grade = "Удовлетворительно"
            color = "#FF9800"
        else:
            icon = "📚"
            grade = "Попробуйте еще раз"
            color = "#F44336"
        
        result_html = f"""
        <div style='text-align: center;'>
            <h1 style='font-size: 72px;'>{icon}</h1>
            <h2 style='color: {color};'>{grade}</h2>
            <h3>Правильных ответов: {self.score} из {len(self.questions)}</h3>
            <h2>Результат: {percentage}%</h2>
        </div>
        """
        
        result_text.setText(result_html)
        layout.addWidget(result_text)
        
        # Детализация ответов
        details = QTextEdit()
        details.setReadOnly(True)
        details_text = "<h3>Детализация ответов:</h3><ol>"
        
        for i, question in enumerate(self.questions):
            details_text += f"<li><b>{question['question']}</b><br>"
            
            if self.correct_answers[i]:
                details_text += "<span style='color: green;'>✓ Верно</span><br>"
            else:
                details_text += "<span style='color: red;'>✗ Неверно</span><br>"
                
                # Показываем правильный ответ
                details_text += "<b>Правильный ответ:</b> "
                correct_options = [f"{chr(65 + idx)}. {question['options'][idx]}" 
                                 for idx in question['correct']]
                details_text += ", ".join(correct_options)
                
                # Показываем объяснение
                details_text += f"<br><i>{question.get('explanation', '')}</i>"
            
            details_text += "</li><hr>"
        
        details_text += "</ol>"
        details.setHtml(details_text)
        layout.addWidget(details)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        close_btn = QPushButton('Закрыть')
        close_btn.clicked.connect(result_window.close)
        
        retry_btn = QPushButton('Пройти заново')
        retry_btn.clicked.connect(lambda: self.retry_test(result_window))
        
        button_layout.addWidget(close_btn)
        button_layout.addWidget(retry_btn)
        
        layout.addLayout(button_layout)
        
        result_window.setLayout(layout)
        result_window.exec_()

    def retry_test(self, window):
        window.close()
        self.current_question = 0
        self.score = 0
        self.answers = []
        self.show_question()


class ResultsWindow(QWidget):
    def __init__(self, username, users):
        super().__init__()
        self.username = username
        self.users = users
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Мои результаты')
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout()
        
        title = QLabel('История тестов')
        title.setFont(QFont('Arial', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        if not self.users[self.username]['tests']:
            no_results = QLabel('Вы еще не проходили тесты')
            no_results.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_results)
        else:
            self.results_table = QTableWidget()
            self.results_table.setColumnCount(4)
            self.results_table.setHorizontalHeaderLabels(['Дата', 'Результат', 'Процент', 'Оценка'])
            self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
            
            self.load_results_to_table()
            layout.addWidget(self.results_table)
            
            # Статистика
            stats = self.calculate_statistics()
            stats_label = QLabel(stats)
            stats_label.setFont(QFont('Arial', 10))
            layout.addWidget(stats_label)
        
        close_btn = QPushButton('Закрыть')
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

    def load_results_to_table(self):
        tests = self.users[self.username]['tests']
        self.results_table.setRowCount(len(tests))
        
        for row, test in enumerate(reversed(tests)):  # Новые тесты сверху
            # Дата
            date_item = QTableWidgetItem(test['date'])
            self.results_table.setItem(row, 0, date_item)
            
            # Результат
            result_item = QTableWidgetItem(f"{test['score']}/{test['total']}")
            result_item.setTextAlignment(Qt.AlignCenter)
            self.results_table.setItem(row, 1, result_item)
            
            # Процент
            percentage = test['percentage']
            percent_item = QTableWidgetItem(f"{percentage}%")
            percent_item.setTextAlignment(Qt.AlignCenter)
            
            # Оценка с цветом
            if percentage >= 90:
                grade = 'Отлично'
                color = QColor(76, 175, 80)  # Зеленый
            elif percentage >= 70:
                grade = 'Хорошо'
                color = QColor(33, 150, 243)  # Синий
            elif percentage >= 50:
                grade = 'Удовл.'
                color = QColor(255, 152, 0)   # Оранжевый
            else:
                grade = 'Неудовл.'
                color = QColor(244, 67, 54)   # Красный
            
            grade_item = QTableWidgetItem(grade)
            grade_item.setForeground(color)
            grade_item.setFont(QFont('Arial', 10, QFont.Bold))
            grade_item.setTextAlignment(Qt.AlignCenter)
            
            self.results_table.setItem(row, 2, percent_item)
            self.results_table.setItem(row, 3, grade_item)
        
        self.results_table.resizeColumnsToContents()

    def calculate_statistics(self):
        tests = self.users[self.username]['tests']
        total_tests = len(tests)
        
        if total_tests == 0:
            return "Нет данных для статистики"
        
        avg_percentage = sum(t['percentage'] for t in tests) / total_tests
        best_score = max(t['percentage'] for t in tests)
        last_score = tests[-1]['percentage'] if tests else 0
        
        stats = f"""
        <b>Статистика:</b><br>
        Всего тестов: {total_tests}<br>
        Средний результат: {avg_percentage:.1f}%<br>
        Лучший результат: {best_score}%<br>
        Последний тест: {last_score}%
        """
        
        return stats