import sys
import os
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QGridLayout
from Minerva_Lite import Configuration, Chemical


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OT2 GUI")
        self.setGeometry(100, 100, 300, 200)

        self.input_inhibitor1 = QLineEdit()
        self.input_vol1 = QLineEdit()
        self.input_inhibitor2 = QLineEdit()
        self.input_vol2 = QLineEdit()
        self.btn_add = QPushButton("Add")
        self.btn_save = QPushButton("Save")

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
        layout.addWidget(self.btn_add, 3, 0, 1, 2)
        layout.addWidget(self.btn_save, 3, 2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connect button click to event handlers
        self.btn_add.clicked.connect(self.add_volumes)
        self.btn_save.clicked.connect(self.save_to_excel)

        # Initialize DataFrame to store data
        self.data = pd.DataFrame(columns=["Inhibitor 1", "Volume 1 [µl]", "Inhibitor 2", "Volume 2 [µl]"])

    def add_volumes(self):
        inhibitor1 = self.input_inhibitor1.text()
        vol1 = float(self.input_vol1.text())
        inhibitor2 = self.input_inhibitor2.text()
        vol2 = float(self.input_vol2.text())

        # Add the data to the DataFrame
        data_to_append = {"Inhibitor 1": inhibitor1, "Volume 1 [µl]": vol1, "Inhibitor 2": inhibitor2, "Volume 2 [µl]": vol2}
        self.data = pd.concat([self.data, pd.DataFrame([data_to_append])], ignore_index=True)

        # Your existing code for the OT2 operation can be added here.
        
        # Reload the last configuration
        Configuration.load_configuration()

        # Rebind the objects that were loaded to variables
        ot2 = Configuration.OpentronsOT2["ot2"]
        corrosion_inhibitor1_container = Configuration.Containers['corrosion_inhibitor1_container']
        corrosion_inhibitor2_container = Configuration.Containers['corrosion_inhibitor2_container']
        target_container = Configuration.Containers['target_container']

        # Define other parameters
        steps = 0
        maximum_steps = 50
        corrosion_current = 10
        target_corrosion_current = 0.01

        while (corrosion_current > target_corrosion_current and steps < maximum_steps):
            corrosion_inhibitor1 = Chemical(container=corrosion_inhibitor1_container, volume=f'{vol1} uL', name='CorrosionInhibitor1')
            corrosion_inhibitor2 = Chemical(container=corrosion_inhibitor2_container, volume=f'{vol2} uL', name='CorrosionInhibitor2')

            # Perform the addition step    
            ot2.add(chemical=[corrosion_inhibitor1, corrosion_inhibitor2], target_container=target_container)

          #  corrosion_current = electrochemistry.measure()
            vol1, vol2 = bayesian_optimizer.suggest_new_parameters(vol1, vol2, corrosion_current)

            steps += 1
        # ...

    def save_to_excel(self):
        file_name = "experiment_data.xlsx"
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, file_name)
        self.data.to_excel(file_path, index=False)
        print(f"Data saved to {file_path}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
