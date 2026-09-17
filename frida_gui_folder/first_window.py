from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QCheckBox, QFileDialog, QHBoxLayout, QVBoxLayout
from PyQt6 import QtCore

from sample_rack import SecondWindow


class FirstWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        #Giving titlle to the window
        self.setWindowTitle("FRIDA Configuration")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: grey;")
        
        #Creating heading to the label
        heading_label = QLabel("FRIDA CONFIGURATION SCREEN")
        heading_label.setStyleSheet("color: black; font-weight: bold; font-size: 20px;")
        
        #Creating configuration button while loads the json file into it
        self.load_config_button = QPushButton("Load Configuration File")
        self.load_config_button.setStyleSheet("background-color: white;")
        
        #Experiment label name of the experiment
        experiment_label = QLabel("Name of the Experiment")
        experiment_label.setStyleSheet("background-color: white;")
        
        #Line edit to write the name of the experiment
        experiment_edit = QLineEdit("Give name to your experiment")
        experiment_edit.setStyleSheet("background-color: light grey;")
        
        #Creating Horizontal layout for experiment_label and experiment_edit
        experiment_layout = QHBoxLayout()
        
        #Adding experiment_label and experiment_edit to experiment_layout which is Horizontal layout
        experiment_layout.addWidget(experiment_label)
        experiment_layout.addWidget(experiment_edit)
        
        #frida method label 
        frida_method_label = QLabel("                           FRIDA Method List")
        frida_method_label.setStyleSheet("font-size: 18px; color: blue; font-weight:bold;")
        
        #Frida configuration label
        frida_config_label = QLabel("                          Configuration Set")
        frida_config_label.setStyleSheet("font-size: 18px; color: blue; font-weight:bold;")
        
        #Frida selection label
        #frida_selection_label = QLabel("Selection")
        
        #Adding Horizontal layout
        frida_layout = QHBoxLayout()
        
        #adding the above three labels in an horizontal layout
        frida_layout.addWidget(frida_method_label)
        frida_layout.addWidget(frida_config_label)
        #frida_layout.addWidget(frida_selection_label)
        
        #Creating Combo box
        self.frida_method_combo = QComboBox()
        self.frida_method_combo.setStyleSheet("background-color: white;")
        self.frida_method_combo.addItems(["Select screen", "Sample Rack", "Electrolyte Preparation", "ElectroChemistry"])
        
        #Button to open the selected window from Combobox
        self.frida_config_combo = QPushButton("Button to open Selected Window")
        self.frida_config_combo.setStyleSheet("background-color: white;")
        self.frida_config_combo.clicked.connect(self.get_selected_items)
        
        # def get_selected_items(self):
        #     #Get the selected items from the combobox
        #     selected_items = []
            
        #     for index in range(self.frida_method_combo.count()):
        #         if self.frida_method_combo.itemText(index) in self.frida_method_combo.currentText():
        #             selected_items.append(self.frida_method_combo.itemText(index))
        

        
        
        #Creating Frida selection checkbox
        #frida_selection_checkbox = QCheckBox()
        #frida_selection_checkbox.setStyleSheet("background-color: white;")

        # Creating Combo box, configuration button and checkbox to the horizontal layout
        frida_combo_layout = QHBoxLayout()
        frida_combo_layout.addWidget(self.frida_method_combo)
        frida_combo_layout.addWidget(self.frida_config_combo)
        #frida_combo_layout.addWidget(frida_selection_checkbox)
        
        #Creating Combo box second row
        frida_method_combo_2 = QComboBox()
        frida_method_combo_2.setStyleSheet("background-color: white;")
        frida_method_combo_2.addItems(["Select screen", "Sample Rack", "Electrolyte Preparation", "ElectroChemistry"])
        
        #Button to open the window we need
        frida_config_combo_2 = QPushButton("Button to open Selected Window")
        frida_config_combo_2.setStyleSheet("background-color: white;")
        
        # Creating Combo box, configuration button and checkbox to the horizontal layout
        frida_combo_layout_2 = QHBoxLayout()
        frida_combo_layout_2.addWidget(frida_method_combo_2)
        frida_combo_layout_2.addWidget(frida_config_combo_2)
        
        #Creating Combo box third row
        frida_method_combo_3 = QComboBox()
        frida_method_combo_3.setStyleSheet("background-color: white;")
        frida_method_combo_3.addItems(["Select screen", "Sample Rack", "Electrolyte Preparation", "ElectroChemistry"])
        
        #Button to open the window we need
        frida_config_combo_3 = QPushButton("Button to open Selected Window")
        frida_config_combo_3.setStyleSheet("background-color: white;")
        
        # Creating Combo box, configuration button and checkbox to the horizontal layout
        frida_combo_layout_3 = QHBoxLayout()
        frida_combo_layout_3.addWidget(frida_method_combo_3)
        frida_combo_layout_3.addWidget(frida_config_combo_3)
        
        #Creating Combo box fourth row
        frida_method_combo_4 = QComboBox()
        frida_method_combo_4.setStyleSheet("background-color: white;")
        frida_method_combo_4.addItems(["Select screen", "Sample Rack", "Electrolyte Preparation", "ElectroChemistry"])
        
        #Button to open the window we need
        frida_config_combo_4 = QPushButton("Button to open Selected Window")
        frida_config_combo_4.setStyleSheet("background-color: white;")
        
        # Creating Combo box, configuration button and checkbox to the horizontal layout
        frida_combo_layout_4 = QHBoxLayout()
        frida_combo_layout_4.addWidget(frida_method_combo_4)
        frida_combo_layout_4.addWidget(frida_config_combo_4)
        
        #Creating Combo box fifth row
        frida_method_combo_5 = QComboBox()
        frida_method_combo_5.setStyleSheet("background-color: white;")
        frida_method_combo_5.addItems(["Select screen", "Sample Rack", "Electrolyte Preparation", "ElectroChemistry"])
        
        #Button to open the window we need
        frida_config_combo_5 = QPushButton("Button to open Selected Window")
        frida_config_combo_5.setStyleSheet("background-color: white;")
        
        # Creating Combo box, configuration button and checkbox to the horizontal layout
        frida_combo_layout_5 = QHBoxLayout()
        frida_combo_layout_5.addWidget(frida_method_combo_5)
        frida_combo_layout_5.addWidget(frida_config_combo_5)
        
        #Creating Combo box sixth row
        frida_method_combo_6 = QComboBox()
        frida_method_combo_6.setStyleSheet("background-color: white;")
        frida_method_combo_6.addItems(["Select screen", "Sample Rack", "Electrolyte Preparation", "ElectroChemistry"])
        
        #Button to open the window we need
        frida_config_combo_6 = QPushButton("Button to open Selected Window")
        frida_config_combo_6.setStyleSheet("background-color: white;")
        
        # Creating Combo box, configuration button and checkbox to the horizontal layout
        frida_combo_layout_6 = QHBoxLayout()
        frida_combo_layout_6.addWidget(frida_method_combo_6)
        frida_combo_layout_6.addWidget(frida_config_combo_6)
        
        #Creating Combo box seventh row
        frida_method_combo_7 = QComboBox()
        frida_method_combo_7.setStyleSheet("background-color: white;")
        frida_method_combo_7.addItems(["Select screen", "Sample Rack", "Electrolyte Preparation", "ElectroChemistry"])
        
        #Button to open the window we need
        frida_config_combo_7 = QPushButton("Button to open Selected Window")
        frida_config_combo_7.setStyleSheet("background-color: white;")
        
        # Creating Combo box, configuration button and checkbox to the horizontal layout
        frida_combo_layout_7 = QHBoxLayout()
        frida_combo_layout_7.addWidget(frida_method_combo_7)
        frida_combo_layout_7.addWidget(frida_config_combo_7)
        
        
        #Creating Combo box eigth row
        frida_method_combo_8 = QComboBox()
        frida_method_combo_8.setStyleSheet("background-color: white;")
        frida_method_combo_8.addItems(["Select screen", "Sample Rack", "Electrolyte Preparation", "ElectroChemistry"])
        
        #Button to open the window we need
        frida_config_combo_8 = QPushButton("Button to open Selected Window")
        frida_config_combo_8.setStyleSheet("background-color: white;")
        
        # Creating Combo box, configuration button and checkbox to the horizontal layout
        frida_combo_layout_8 = QHBoxLayout()
        frida_combo_layout_8.addWidget(frida_method_combo_8)
        frida_combo_layout_8.addWidget(frida_config_combo_8)
        
        #Creating Combo box nineth row
        frida_method_combo_9 = QComboBox()
        frida_method_combo_9.setStyleSheet("background-color: white;")
        frida_method_combo_9.addItems(["Select screen", "Sample Rack", "Electrolyte Preparation", "ElectroChemistry"])
        
        #Button to open the window we need
        frida_config_combo_9 = QPushButton("Button to open Selected Window")
        frida_config_combo_9.setStyleSheet("background-color: white;")
        
        # Creating Combo box, configuration button and checkbox to the horizontal layout
        frida_combo_layout_9 = QHBoxLayout()
        frida_combo_layout_9.addWidget(frida_method_combo_9)
        frida_combo_layout_9.addWidget(frida_config_combo_9)        
        
        #Creating Combo box tenth row
        frida_method_combo_10 = QComboBox()
        frida_method_combo_10.setStyleSheet("background-color: white;")
        frida_method_combo_10.addItems(["Select screen", "Sample Rack", "Electrolyte Preparation", "ElectroChemistry"])
        
        #Button to open the window we need
        frida_config_combo_10 = QPushButton("Button to open Selected Window")
        frida_config_combo_10.setStyleSheet("background-color: white;")
        
        # Creating Combo box, configuration button and checkbox to the horizontal layout
        frida_combo_layout_10 = QHBoxLayout()
        frida_combo_layout_10.addWidget(frida_method_combo_10)
        frida_combo_layout_10.addWidget(frida_config_combo_10)
        
        #Creating Combo box eleventh row
        frida_method_combo_11 = QComboBox()
        frida_method_combo_11.setStyleSheet("background-color: white;")
        frida_method_combo_11.addItems(["Select screen", "Sample Rack", "Electrolyte Preparation", "ElectroChemistry"])
        
        #Button to open the window we need
        frida_config_combo_11 = QPushButton("Button to open Selected Window")
        frida_config_combo_11.setStyleSheet("background-color: white;")
        
        # Creating Combo box, configuration button and checkbox to the horizontal layout
        frida_combo_layout_11 = QHBoxLayout()
        frida_combo_layout_11.addWidget(frida_method_combo_11)
        frida_combo_layout_11.addWidget(frida_config_combo_11)
        
        #Creating Combo box twelveth row
        frida_method_combo_12 = QComboBox()
        frida_method_combo_12.setStyleSheet("background-color: white;")
        frida_method_combo_12.addItems(["Select screen", "Sample Rack", "Electrolyte Preparation", "ElectroChemistry"])
        
        #Button to open the window we need
        frida_config_combo_12 = QPushButton("Button to open Selected Window")
        frida_config_combo_12.setStyleSheet("background-color: white;")
        
        # Creating Combo box, configuration button and checkbox to the horizontal layout
        frida_combo_layout_12 = QHBoxLayout()
        frida_combo_layout_12.addWidget(frida_method_combo_12)
        frida_combo_layout_12.addWidget(frida_config_combo_12)


        # configuration button
        open_config_button = QPushButton("Open Configuration Screen")
        open_config_button.setStyleSheet("background-color: white;")
        
        #Load dataset button
        self.use_prev_dataset_button = QPushButton("Use Previous Dataset")
        self.use_prev_dataset_button.setStyleSheet("background-color: white;")
        
        #Save data button and move to the next screen button
        save_data_button = QPushButton("Save Data and Move to FRIDA Screen")
        save_data_button.setStyleSheet("background-color: light blue;")
        
        #Adding use previous dataset button and save button in Horizontal layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(open_config_button)
        button_layout.addWidget(self.use_prev_dataset_button)
        
        #Creating vertical layout object
        layout = QVBoxLayout()
        
        #Adding the labels and other widgets in vertical box layout
        layout.addWidget(heading_label)
        layout.addWidget(self.load_config_button)
        layout.addLayout(experiment_layout)
        layout.addLayout(frida_layout)
        layout.addLayout(frida_combo_layout)
        layout.addLayout(frida_combo_layout_2)
        layout.addLayout(frida_combo_layout_3)
        layout.addLayout(frida_combo_layout_4)
        layout.addLayout(frida_combo_layout_5)
        layout.addLayout(frida_combo_layout_6)
        layout.addLayout(frida_combo_layout_7)
        layout.addLayout(frida_combo_layout_8)
        layout.addLayout(frida_combo_layout_9)
        layout.addLayout(frida_combo_layout_10)
        layout.addLayout(frida_combo_layout_11)
        layout.addLayout(frida_combo_layout_12)
        layout.addLayout(button_layout)
        layout.addWidget(save_data_button)
        self.setLayout(layout)

        # Connecting signals to slots
        self.load_config_button.clicked.connect(self.load_config_file)
        self.use_prev_dataset_button.clicked.connect(self.load_csv_data)
        save_data_button.clicked.connect(self.save_data_and_move_to_second_window)
        
    def load_config_file(self):
        file_dialog = QFileDialog()
        json_file_path, _ = file_dialog.getOpenFileName(self, "load json file", "", "JSON Files(*.json)")
        if json_file_path:
            self.load_config_button.setText(json_file_path)
            print(json_file_path, "has been loaded")

    def load_csv_data(self):
        file_csv_dialog = QFileDialog()
        csv_file_path, _ = file_csv_dialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if csv_file_path:
            self.use_prev_dataset_button.setText(csv_file_path)
            print(csv_file_path, "has uploaded")
    
    #function to open the selected window from the combo box by cling the button        
    def get_selected_items(self):
        #create an instance that we select the window at the Combo box
        selected_item = self.frida_method_combo.currentText()
        if selected_item == "Sample Rack":
            self.second_window = SecondWindow()
            self.second_window.show()      

    def save_data_and_move_to_second_window(self):
    # Save the data from the first window
    # Create an instance of the second window and show it
        # selected_items = self.get_selected_items()
        # if "Sample Rack" in selected_items:
        self.second_window = SecondWindow()
        self.second_window.show()
    
        # Close the first window
        #self.close()
