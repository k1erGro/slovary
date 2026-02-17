import sys
import os
import sys
import site

# Автоматический поиск папки с плагинами Qt
def setup_qt_plugins():
    possible_paths = []
    
    # В виртуальном окружении
    possible_paths.append(os.path.join(sys.prefix, 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins'))
    possible_paths.append(os.path.join(sys.prefix, 'Lib', 'site-packages', 'PyQt5', 'plugins'))
    
    # В глобальных site-packages
    for sp in site.getsitepackages():
        possible_paths.append(os.path.join(sp, 'PyQt5', 'Qt5', 'plugins'))
        possible_paths.append(os.path.join(sp, 'PyQt5', 'plugins'))
    
    for path in possible_paths:
        if os.path.isdir(os.path.join(path, 'platforms')):
            os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = path
            print(f"✅ Найден путь к плагинам: {path}")
            return True
    
    # Если не нашли, выводим подсказку
    print("❌ Не удалось найти папку plugins. Укажите путь вручную.")
    return False

setup_qt_plugins()

# Теперь можно импортировать PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Импортируем модули
from Module1 import AuthWindow
from Module2 import TheoryWindow
from Module3 import TestWindow, ResultsWindow

class MainWindow(QMainWindow):
    def __init__(self, username, users):
        super().__init__()
        self.username = username
        self.users = users
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f'Изучение словарей Python - {self.username}')
        self.setFixedSize(500, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel(f'Добро пожаловать, {self.username}!')
        title.setFont(QFont('Arial', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('color: #2c3e50; padding: 20px;')
        layout.addWidget(title)
        
        # Информация о пользователе
        user_info = QLabel(f'Зарегистрирован: {self.users[self.username]["created_at"]}')
        user_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(user_info)
        
        # Кнопки выбора
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 15px;
                font-size: 14px;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        
        theory_btn = QPushButton('📚 Изучить теорию')
        theory_btn.setStyleSheet(button_style)
        theory_btn.clicked.connect(self.open_theory)
        
        test_btn = QPushButton('✏️ Пройти тест')
        test_btn.setStyleSheet(button_style)
        test_btn.clicked.connect(self.open_test)
        
        results_btn = QPushButton('📊 Мои результаты')
        results_btn.setStyleSheet(button_style)
        results_btn.clicked.connect(self.show_results)
        
        layout.addWidget(theory_btn)
        layout.addWidget(test_btn)
        layout.addWidget(results_btn)
        
        # Статистика
        stats_text = self.get_user_stats()
        self.stats_label = QLabel(stats_text)
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setWordWrap(True)
        self.stats_label.setStyleSheet('background-color: #ecf0f1; padding: 10px; border-radius: 5px;')
        layout.addWidget(self.stats_label)
        
        # Выход
        logout_btn = QPushButton('🚪 Выйти')
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)
        
        central_widget.setLayout(layout)

    def get_user_stats(self):
        tests = self.users[self.username]['tests']
        if not tests:
            return "Вы еще не проходили тесты"
        
        last_test = tests[-1]
        total_tests = len(tests)
        avg_score = sum(t['score'] for t in tests) / total_tests
        best_score = max(t['score'] for t in tests)
        return (f"Всего тестов пройдено: {total_tests}\n"
                f"Последний результат: {last_test['score']}/{last_test['total']}\n"
                f"Средний балл: {avg_score:.1f}\n"
                f"Лучший результат: {best_score}/{last_test['total']}")

    def open_theory(self):
        self.theory_window = TheoryWindow()
        self.theory_window.show()

    def open_test(self):
        self.test_window = TestWindow(self.username, self.users)
        self.test_window.show()

    def show_results(self):
        self.results_window = ResultsWindow(self.username, self.users)
        self.results_window.show()

    def logout(self):
        self.auth_window = AuthWindow()
        self.auth_window.show()
        self.close()


def main():
    app = QApplication(sys.argv)
    
    # Установка стиля
    app.setStyle('Fusion')
    
    # Настройка палитры
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    app.setPalette(palette)
    
    # Запуск окна авторизации
    auth = AuthWindow()
    auth.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()