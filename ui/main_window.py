from PyQt5.QtWidgets import QMainWindow, QTextEdit, QListWidget, QPushButton, QWidget, QHBoxLayout, QInputDialog
from models.note import Note

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("note-taking-app")
        self.editor = QTextEdit(self)
        self.notes_list = QListWidget(self)
        self.add_note_button = QPushButton("Add", self)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        hbox = QHBoxLayout()

        hbox.addWidget(self.editor, 2)
        hbox.addWidget(self.notes_list, 1)
        hbox.addWidget(self.add_note_button)

        central_widget.setLayout(hbox)

        self.add_note_button.clicked.connect(self.add_note) 

    def add_note(self):
        note_title, confirmation = QInputDialog.getText(self, "New Note", "Enter note title:")
        if note_title and confirmation:
            new_note = Note(note_title, "")
            self.notes_list.addItem(new_note.title)
