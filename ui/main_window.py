import os
import json
import shutil

from PyQt5.QtWidgets import (
    QMainWindow,
    QTextEdit,
    QListWidget,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QInputDialog,
    QShortcut,
    QMessageBox,
)
from PyQt5.QtGui import QIcon, QKeySequence

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

        # Shortcuts
        self.add_note_shortcut = QShortcut(QKeySequence("Ctrl+Shift+A"), self)
        self.delete_note_shortcut = QShortcut(
            QKeySequence("Ctrl+Shift+D"), self)
        self.rename_note_shortcut = QShortcut(
            QKeySequence("Ctrl+Shift+R"), self)
        self.save_all_notes_shortcut = QShortcut(
            QKeySequence("Ctrl+Shift+S"), self)
        self.toggle_theme_mode_shortcut = QShortcut(
            QKeySequence("Ctrl+Shift+T"), self)

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

        # Add buttons vertically
        vbox.addWidget(self.add_note_button)
        vbox.addWidget(self.delete_note_button)
        vbox.addWidget(self.theme_toggle_button)

        hbox.addWidget(self.editor, 2)
        hbox.addWidget(self.notes_list, 1)
        hbox.addLayout(vbox)

        self.theme_toggle_button.setIcon(
            QIcon("assets/light_mode_sun_icon.png"))

        central_widget.setLayout(hbox)

        # Connect signals to slots
        self.add_note_button.clicked.connect(self.add_note)
        self.delete_note_button.clicked.connect(self.delete_note)
        self.theme_toggle_button.clicked.connect(self.toggle_theme_mode)
        self.notes_list.itemClicked.connect(self.display_content)
        self.editor.textChanged.connect(self.save_content)
        self.notes_list.itemDoubleClicked.connect(self.rename_note)

        self.add_note_shortcut.activated.connect(self.add_note)
        self.delete_note_shortcut.activated.connect(self.delete_note)
        self.rename_note_shortcut.activated.connect(self.rename_note)
        self.save_all_notes_shortcut.activated.connect(self.save_all_notes)
        self.toggle_theme_mode_shortcut.activated.connect(
            self.toggle_theme_mode)

    def add_note(self):
        """
        Prompt the user to enter a new note title,
        then add the note to the list and enable editing.
        """
        note_title, confirmation = QInputDialog.getText(
            self, "New Note", "Enter note title:")

        if not confirmation:
            return

        if any(note.title == note_title for note in self.notes):
            QMessageBox.warning(
                self,
                "Duplicate Title",
                "A note with this title already exists.")
            return

        new_note = Note(title=note_title, content="")
        self.notes.append(new_note)
        self.notes_list.addItem(new_note.title)
        self.notes_list.setCurrentRow(self.notes_list.count() - 1)
        self.display_content(self.notes_list.currentItem())
        self.editor.setDisabled(False)

    def load_notes(self):
        """Load notes from a JSON file and populate the list widget."""
        notes_data = []

        if not os.path.isfile(
                self.file_path) or os.path.getsize(
                self.file_path) == 0:
            return

        try:
            with open(self.file_path, "r") as data_file:
                notes_data = json.load(data_file)
        except json.JSONDecodeError:
            backup_path = self.file_path + ".backup"
            shutil.copy(self.file_path, backup_path)
            QMessageBox.critical(
                self,
                "Loading Error",
                (
                    "An unexpected error occurred during loading.\n\n"
                    f"A backup of the file has been created at:\n{backup_path}"
                ),
            )
            return

        for data in notes_data:
            note = Note.from_dict(data)
            self.notes.append(note)
            self.notes_list.addItem(note.title)

    def display_content(self, item):
        """Display the content of the selected note in the editor."""
        if item is None:
            self.editor.clear()
            self.editor.setDisabled(True)
            return

        self.selected_note = item.text()

        for note in self.notes:
            if note.title == self.selected_note:
                self.editor.setPlainText(note.content or "")
                self.editor.setDisabled(False)
                return

        self.editor.clear()
        self.editor.setDisabled(True)

    def save_content(self):
        """Save the current editor content to the selected note."""
        if not self.selected_note:
            return

        try:
            new_content = self.editor.toPlainText()
            for note in self.notes:
                if note.title == self.selected_note:
                    note.content = new_content
                    break
            self.save_all_notes()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Save Error",
                f"An error occurred while saving the note content.\n\n{
                    str(e)}",
            )

    def delete_note(self):
        """Remove the selected note after user confirmation and update UI and storage."""
        if not self.selected_note:
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the note '{
                self.selected_note}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirm != QMessageBox.Yes:
            return

        try:
            self.notes = [
                note for note in self.notes if note.title != self.selected_note]
            self.refresh_notes_list()
            self.selected_note = None
            self.editor.clear()
            self.editor.setDisabled(True)
            self.save_all_notes()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Delete Error",
                f"An error occurred while deleting the note.\n\n{str(e)}",
            )

    def rename_note(self):
        """Prompt to rename the selected note and update the UI."""
        note_title, confirmation = QInputDialog.getText(
            self, "Rename title", "Enter new note title:"
        )

        if not confirmation:
            return

        if any(note.title == note_title for note in self.notes):
            QMessageBox.warning(
                self,
                "Duplicate Title",
                "A note with this title already exists.",
            )
            return

        try:
            for note in self.notes:
                if note.title == self.selected_note:
                    note.title = note_title
                    break

            self.refresh_notes_list()
            self.selected_note = None
            self.editor.clear()
            self.editor.setDisabled(True)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Rename Error",
                f"An unexpected error occurred while renaming the note.\n\n{
                    str(e)}",
            )

    def refresh_notes_list(self):
        """Clear and reload the note titles in the list widget."""
        try:
            self.notes_list.clear()
            for note in self.notes:
                self.notes_list.addItem(note.title)
        except Exception as e:
            QMessageBox.critical(
                self,
                "List Refresh Error",
                f"An error occurred while refreshing the notes list.\n\n{
                    str(e)}",
            )

    def save_all_notes(self):
        """Serialize all notes and save them to the JSON file."""
        try:
            notes_data = [note.to_dict() for note in self.notes]
            with open(self.file_path, "w") as data:
                json.dump(notes_data, data, indent=4)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Save All Notes Error",
                f"An error occurred while saving notes.\n\n{str(e)}",
            )

    def toggle_theme_mode(self):
        """Toggle between light and dark themes and update the UI icon."""
        self.dark_mode = not self.dark_mode

        theme = dark_theme if self.dark_mode else light_theme
        icon_path = "assets/dark_mode_moon_icon.png" if self.dark_mode else "assets/light_mode_sun_icon.png"

        self.setStyleSheet(theme)
        self.theme_toggle_button.setIcon(QIcon(icon_path))
