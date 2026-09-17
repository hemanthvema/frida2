import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class OT2GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OT2 GUI")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        # Row 1
        channel_label = QLabel("Channel")
        channel_label.setStyleSheet("color: green;")
        grid_layout.addWidget(channel_label, 0, 0)

        name_label = QLabel("NAME")
        name_label.setStyleSheet("color: blue;")
        grid_layout.addWidget(name_label, 0, 1)

        volume_label = QLabel("Volume(μl)")
        volume_label.setStyleSheet("color: red;")
        grid_layout.addWidget(volume_label, 0, 2)

        # Row 2
        inhibitor1_label = QLabel("Inhibitor 1")
        grid_layout.addWidget(inhibitor1_label, 1, 0)

        inhibitor1_line_edit = QLineEdit()
        grid_layout.addWidget(inhibitor1_line_edit, 1, 1)

        inhibitor1_int_edit = QLineEdit()
        grid_layout.addWidget(inhibitor1_int_edit, 1, 2)

        # Row 3
        inhibitor2_label = QLabel("Inhibitor 2")
        grid_layout.addWidget(inhibitor2_label, 2, 0)

        inhibitor2_line_edit = QLineEdit()
        grid_layout.addWidget(inhibitor2_line_edit, 2, 1)

        inhibitor2_int_edit = QLineEdit()
        grid_layout.addWidget(inhibitor2_int_edit, 2, 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OT2GUI()
    window.show()
    sys.exit(app.exec())
