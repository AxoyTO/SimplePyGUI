from PyQt5.QtWidgets import QApplication
from app import *

app = QApplication([])

window = MainWindow()
window.show()

app.exec()
