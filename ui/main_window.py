from PyQt5.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("note-taking-app")
        self.showMaximized()
        self.initUI()

    def initUI(self):
        pass
