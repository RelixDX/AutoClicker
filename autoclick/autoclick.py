# Importar bibliotecas
import sys
import threading
import pyautogui as pg
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit
import keyboard

# Criar a classe do auto click


class AutoClick:
    def __init__(self):
        self.running = False
        self.thread = None
        self.cursor = True

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()

    def lock_cursor(self):
        self.cursor = not self.cursor

    def run(self):
        screen_center = (pg.size().width / 2, pg.size().height / 2)
        while self.running:
            if self.cursor:
                pg.click()
            else:
                pg.click(screen_center)
            pg.sleep(0.001)

# Criar função de ligar e desligar o auto click


def toggle_clicker(clicker):
    if clicker.running:
        clicker.stop()
    else:
        clicker.start()

# Criar a classe do GUI


class ClickerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.clicker = AutoClick()
        self.hotkey = '-'  # Tecla padrão
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle('AutoClicker')

        layout = QVBoxLayout()

        self.hotkey_input = QLineEdit(self)
        self.hotkey_input.setPlaceholderText(
            'Digite a tecla para ligar/desligar')
        self.hotkey_input.textChanged.connect(self.update_hotkey)
        layout.addWidget(self.hotkey_input)

        self.start_button = QPushButton(
            f'Pressione {self.hotkey} para iniciar', self)
        self.start_button.clicked.connect(self.clicker.start)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton(
            f'Pressione {self.hotkey} para parar', self)
        self.stop_button.clicked.connect(self.clicker.stop)
        layout.addWidget(self.stop_button)

        self.cursor_button = QPushButton(self.cursor_button_text(), self)
        self.cursor_button.clicked.connect(self.cursor_locked)
        layout.addWidget(self.cursor_button)

        self.setLayout(layout)

        keyboard.add_hotkey(self.hotkey, toggle_clicker, args=(self.clicker,))

    def update_hotkey(self, text):
        new_hotkey = text.strip()
        if new_hotkey and new_hotkey != self.hotkey:
            keyboard.remove_hotkey(self.hotkey)
            self.hotkey = new_hotkey
            keyboard.add_hotkey(
                self.hotkey, toggle_clicker, args=(self.clicker,))

    def cursor_locked(self):
        self.clicker.lock_cursor()
        self.cursor_button.setText(self.cursor_button_text())

    def cursor_button_text(self):
        return 'cursor liberado' if self.clicker.cursor else 'cursor travado'

    def closeEvent(self, event):
        self.clicker.stop()
        keyboard.remove_all_hotkeys()
        event.accept()

# Criar função main


def main():
    app = QApplication(sys.argv)
    clicker_app = ClickerApp()
    clicker_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
