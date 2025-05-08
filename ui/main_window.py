from PyQt5.QtWidgets import QMainWindow, QListWidget, QLineEdit, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("note-taking-app")
        self.setGeometry(0, 0, 1920, 1080)

    def initUI(self):
        # widgets for layout
        self.notes_list = QListWidget()
        self.notes_editor = QLineEdit()

        # layout distribution
        hbox = QHBoxLayout()
        hbox.addWidget(self.notes_list, 1)
        hbox.addWidget(self.notes_editor, 2)

        self.setLayout(hbox)
