import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

from ui.main_window import MainWindow


def main():
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(
            None,
            "Startup Error",
            f"An unexpected error occurred during startup:\n{str(e)}",
        )


if __name__ == "__main__":
    main()
