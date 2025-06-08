import os
import json

from PyQt5.QtWidgets import (
    QMainWindow,
    QTextEdit,
    QListWidget,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QInputDialog,
)
from PyQt5.QtGui import QIcon

from models.note import Note
from ui.themes import dark_theme, light_theme


class MainWindow(QMainWindow):
    def __init__(self):
        """Initialize the main window and UI components."""
        super().__init__()
        self.setWindowTitle("note-taking-app")
        self.setWindowIcon(QIcon("assets/note-taking-app_icon.png"))

        # Widgets
        self.editor = QTextEdit(self)
        self.notes_list = QListWidget(self)
        self.add_note_button = QPushButton("Add", self)
        self.delete_note_button = QPushButton("Delete", self)
        self.theme_toggle_button = QPushButton(self)

        # Data and state
        self.notes = []
        self.file_path = os.path.join("data", "notes.json")
        self.selected_note = None
        self.dark_mode = False

        self.load_notes()
        self.editor.setDisabled(True)

        self.initUI()

    def initUI(self):
        """Set up the UI layout and signal-slot connections."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setStyleSheet(light_theme)

        # Layout container
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        # Add widgets with stretch factors for resizing
        vbox.addWidget(self.add_note_button)
        vbox.addWidget(self.delete_note_button)
        vbox.addWidget(self.theme_toggle_button)
        
        hbox.addWidget(self.editor, 2)
        hbox.addWidget(self.notes_list, 1)
        hbox.addLayout(vbox)

        self.theme_toggle_button.setIcon(QIcon("assets/light_mode_sun_icon.png"))

        central_widget.setLayout(hbox)

        # Connect signals to slots
        self.add_note_button.clicked.connect(self.add_note)
        self.delete_note_button.clicked.connect(self.delete_note)
        self.theme_toggle_button.clicked.connect(self.toggle_theme_mode)
        self.notes_list.itemClicked.connect(self.display_content)
        self.editor.textChanged.connect(self.save_content)
        self.notes_list.itemDoubleClicked.connect(self.rename_note)

    def add_note(self):
        """
        Prompt the user to enter a new note title,
        then add the note to the list and enable editing.
        """
        note_title, confirmation = QInputDialog.getText(self, "New Note", "Enter note title:")

        if note_title and confirmation:
            new_note = Note(title=note_title, content="")

            self.notes.append(new_note)
            self.notes_list.addItem(new_note.title)
            self.notes_list.setCurrentRow(self.notes_list.count() - 1)
            self.display_content(self.notes_list.currentItem())

            self.editor.setDisabled(False)

    def load_notes(self):
        """Load notes from a JSON file and populate the list widget."""
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
        """Display the content of the selected note in the editor."""
        self.selected_note = item.text()

        for note in self.notes:
            if note.title == self.selected_note:
                self.editor.setPlainText(note.content or "")
                self.editor.setDisabled(False)
                break

    def save_content(self):
        """Save the current editor content to the selected note."""
        new_content = self.editor.toPlainText()
        for note in self.notes:
            if note.title == self.selected_note:
                note.content = new_content
                break
        self.save_all_notes()

    def refresh_notes_list(self):
        """Clear and reload the note titles in the list widget."""
        self.notes_list.clear()
        for note in self.notes:
            self.notes_list.addItem(note.title)

    def delete_note(self):
        """Remove the selected note and update the UI and storage."""
        self.notes = [note for note in self.notes if note.title != self.selected_note]
        self.refresh_notes_list()
        self.selected_note = None
        self.editor.clear()
        self.editor.setDisabled(True)
        
    def rename_note(self):
        note_title, confirmation = QInputDialog.getText(self, "Rename title", "Enter note title:")

        if note_title and confirmation:
            for note in self.notes:
                if note.title == self.selected_note:
                    note.title = note_title
                    break
            
            self.refresh_notes_list()
            self.selected_note = None
            self.editor.clear()
            self.editor.setDisabled(True)

    def save_all_notes(self):
        """Serialize all notes and save them to the JSON file."""
        notes_data = [note.to_dict() for note in self.notes]
        with open(self.file_path, "w") as data:
            json.dump(notes_data, data, indent=4)

    def toggle_theme_mode(self):
        """Toggle between light and dark themes and update the UI icon."""
        self.dark_mode = not self.dark_mode

        theme = dark_theme if self.dark_mode else light_theme
        icon_path = "assets/dark_mode_moon_icon.png" if self.dark_mode else "assets/light_mode_sun_icon.png"

        self.setStyleSheet(theme)
        self.theme_toggle_button.setIcon(QIcon(icon_path))
