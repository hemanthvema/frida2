from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton


class SecondWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sample Rack Configuration Screen")

        heading_label = QLabel("Sample Rack Configuration Screen")
        heading_label.setStyleSheet("background-color: grey; color: black; font-weight: bold;")

        num_samples_label = QLabel("Number of Samples: ")
        self.num_samples_edit = QLineEdit("26")
        self.num_samples_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.num_samples_save_btn = QPushButton("Save")

        num_samples_layout = QHBoxLayout()
        num_samples_layout.addWidget(num_samples_label)
        num_samples_layout.addWidget(self.num_samples_edit)
        num_samples_layout.addWidget(self.num_samples_save_btn)

        save_and_continue_btn = QPushButton("Save and Continue")

        main_layout = QVBoxLayout()
        main_layout.addWidget(heading_label)
        main_layout.addSpacing(10)
        main_layout.addLayout(num_samples_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(save_and_continue_btn)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(main_layout)
