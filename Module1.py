import json
import hashlib
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class RegisterWindow(QDialog):
    def __init__(self, users, users_file, parent=None):
        super().__init__(parent)
        self.users = users
        self.users_file = users_file
        self.setWindowTitle('Регистрация нового пользователя')
        self.setFixedSize(350, 250)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel('Регистрация')
        title.setFont(QFont('Arial', 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Введите логин')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Введите пароль')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText('Повторите пароль')
        self.confirm_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow('Логин:', self.username_input)
        form_layout.addRow('Пароль:', self.password_input)
        form_layout.addRow('Подтверждение:', self.confirm_input)

        layout.addLayout(form_layout)

        self.status_label = QLabel('')
        self.status_label.setStyleSheet('color: red;')
        layout.addWidget(self.status_label)

        button_layout = QHBoxLayout()
        register_btn = QPushButton('Зарегистрироваться')
        register_btn.clicked.connect(self.register)
        cancel_btn = QPushButton('Отмена')
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(register_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()

        if not username or not password or not confirm:
            self.status_label.setText('Заполните все поля!')
            return

        if username in self.users:
            self.status_label.setText('Пользователь уже существует!')
            return

        if password != confirm:
            self.status_label.setText('Пароли не совпадают!')
            return

        if len(password) < 4:
            self.status_label.setText('Пароль должен быть не менее 4 символов!')
            return

        self.users[username] = {
            'password': self.hash_password(password),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tests': []
        }

        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=2, ensure_ascii=False)

        QMessageBox.information(self, 'Успех', 'Регистрация прошла успешно!')
        self.accept()


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.users_file = 'users.json'
        self.current_user = None
        self.users = {}
        self.init_ui()
        self.load_users()

    def init_ui(self):
        self.setWindowTitle('Авторизация - Словари Python')
        self.setFixedSize(400, 250)

        layout = QVBoxLayout()

        title = QLabel('Вход в систему')
        title.setFont(QFont('Arial', 16))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Введите логин')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Введите пароль')
        self.password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow('Логин:', self.username_input)
        form_layout.addRow('Пароль:', self.password_input)

        layout.addLayout(form_layout)

        self.status_label = QLabel('')
        self.status_label.setStyleSheet('color: red;')
        layout.addWidget(self.status_label)

        button_layout = QHBoxLayout()
        self.login_btn = QPushButton('Войти')
        self.login_btn.clicked.connect(self.login)
        self.register_btn = QPushButton('Регистрация')
        self.register_btn.clicked.connect(self.open_register)

        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.register_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_users(self):
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.status_label.setText('Заполните все поля!')
            return

        if username in self.users:
            hashed = self.hash_password(password)
            if self.users[username]['password'] == hashed:
                self.current_user = username
                self.status_label.setText('Успешный вход!')
                self.status_label.setStyleSheet('color: green;')
                QTimer.singleShot(500, self.open_main_window)
            else:
                self.status_label.setText('Неверный пароль!')
        else:
            self.status_label.setText('Пользователь не найден!')

    def open_register(self):
        reg_window = RegisterWindow(self.users, self.users_file, self)
        if reg_window.exec() == QDialog.Accepted:
            # после успешной регистрации можно очистить поля или просто сообщить
            self.status_label.setText('Регистрация успешна, теперь войдите.')
            self.status_label.setStyleSheet('color: green;')

    def open_main_window(self):
        from main import MainWindow
        self.main_window = MainWindow(self.current_user, self.users)
        self.main_window.show()
        self.close()