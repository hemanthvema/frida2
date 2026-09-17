import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QGridLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OT2 GUI")
        self.setGeometry(100, 100, 300, 200)

        self.input_vol1 = QLineEdit()
        self.input_vol2 = QLineEdit()
        self.input_inhibitor1 = QLineEdit()
        self.input_inhibitor2 = QLineEdit()
        self.btn_add = QPushButton("Add")

        layout = QGridLayout()
        layout.addWidget(QLabel("Channel"), 0, 0)
        layout.addWidget(QLabel("Name"), 0, 1)
        layout.addWidget(QLabel("Volume [µl]"), 0, 2)
        layout.addWidget(QLabel("Inhibitor 1"), 1, 0)
        layout.addWidget(self.input_inhibitor1, 1, 1)
        layout.addWidget(self.input_vol1, 1, 2)
        layout.addWidget(QLabel("Inhibitor 2"), 2, 0)
        layout.addWidget(self.input_inhibitor2, 2, 1)
        layout.addWidget(self.input_vol2, 2, 2)
        layout.addWidget(self.btn_add, 3, 0, 1, 3)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connect button click to event handler
        self.btn_add.clicked.connect(self.add_volumes)

    def add_volumes(self):
        vol1 = float(self.input_vol1.text())  # Get the value for vol1 from the input field
        vol2 = float(self.input_vol2.text())  # Get the value for vol2 from the input field

        # Update the vol1 and vol2 values in the test.py code
        with open("test.py", "r+") as file:
            code = file.read()
            code = code.replace("vol1 = 60.0", f"vol1 = {vol1}")  # Assuming the initial value in test.py is 60.0
            code = code.replace("vol2 = 80.0", f"vol2 = {vol2}")  # Assuming the initial value in test.py is 80.0
            file.seek(0)
            file.write(code)
            file.truncate()

        # Run the modified test.py code
        exec(open("test.py").read())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
