import sys
from PyQt6.QtWidgets import QApplication
from first_window import FirstWindow
#from sample_rack import SecondWindow
if __name__ == '__main__':
    app = QApplication(sys.argv)
    first_window = FirstWindow()
    first_window.show()
    sys.exit(app.exec())
