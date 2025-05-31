from PyQt5.QtWidgets import QMainWindow, QTextEdit, QListWidget, QPushButton, QWidget, QHBoxLayout, QInputDialog
from models.note import Note
import os
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("note-taking-app")
        self.editor = QTextEdit(self)
        self.notes_list = QListWidget(self)
        self.add_note_button = QPushButton("Add", self)
        self.notes = []
        self.file_path = os.path.join("data", "notes.json")
        self.load_notes()
        self.selected_note = None
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
        self.notes_list.itemClicked.connect(self.display_content)
        self.editor.textChanged.connect(self.save_content)

    def add_note(self):
        note_title, confirmation = QInputDialog.getText(self, "New Note", "Enter note title:")
        
        if note_title and confirmation:
            content = self.editor.toPlainText()
            new_note = Note(title=note_title, content=content)
            
            self.notes_list.addItem(new_note.title)
            self.save_note(new_note)
    
    def save_note(self, note):
        if os.path.getsize(self.file_path) > 0:
            with open(self.file_path, "r") as data:
                notes_data = json.load(data)
        else:
            return
        
        notes_data.append(note.to_dict())

        with open(self.file_path, "w") as data:
            json.dump(notes_data, data, indent=4)

    def load_notes(self):
        if os.path.getsize(self.file_path) > 0:
            with open(self.file_path, "r") as data:
                notes_data = json.load(data)
        else:
            return

        for data in notes_data:
            note = Note.from_dict(data)
            self.notes.append(note)
            self.notes_list.addItem(note.title)
        
    def display_content(self, item):
        self.selected_note = item.text()

        for note in self.notes:
            if note.title == self.selected_note:
                self.editor.setPlainText(note.content)
                break
        
        self.editor.textChanged.connect(self.save_content)
    
    def save_content(self):
        new_content = self.editor.toPlainText()

        for note in self.notes:
            if note.title == self.selected_note:
                note.content = new_content
                break
        
        notes_data = [note.to_dict() for note in self.notes]

        with open(self.file_path, "w") as data:
            json.dump(notes_data, data, indent=4)
