import pandas as pd
import os
from Minerva_Lite import Configuration, Chemical

class BackendExperiment:
    def __init__(self):
        # Initialize DataFrame to store data
        self.data = pd.DataFrame(columns=["Inhibitor 1", "Volume 1 [µl]", "Inhibitor 2", "Volume 2 [µl]"])

        # Load the last configuration
        Configuration.load_configuration()

        # Rebind the objects that were loaded to variables
        self.ot2 = Configuration.OpentronsOT2["ot2"]
        self.corrosion_inhibitor1_container = Configuration.Containers['corrosion_inhibitor1_container']
        self.corrosion_inhibitor2_container = Configuration.Containers['corrosion_inhibitor2_container']
        self.target_container = Configuration.Containers['target_container']

    def add_volumes(self, inhibitor1, vol1, inhibitor2, vol2):
        # Add the data to the DataFrame
        data_to_append = {"Inhibitor 1": inhibitor1, "Volume 1 [µl]": vol1, "Inhibitor 2": inhibitor2, "Volume 2 [µl]": vol2}
        self.data = pd.concat([self.data, pd.DataFrame([data_to_append])], ignore_index=True)

        # Define other parameters
        steps = 0
        maximum_steps = 1
        corrosion_current = 10
        target_corrosion_current = 0.01

        while (corrosion_current > target_corrosion_current and steps < maximum_steps):
            corrosion_inhibitor1 = Chemical(container=self.corrosion_inhibitor1_container, volume=f'{vol1} uL', name='CorrosionInhibitor1')
            corrosion_inhibitor2 = Chemical(container=self.corrosion_inhibitor2_container, volume=f'{vol2} uL', name='CorrosionInhibitor2')

            # Perform the addition step    
            self.ot2.add(chemical=[corrosion_inhibitor1, corrosion_inhibitor2], target_container=self.target_container)

            # corrosion_current = electrochemistry.measure()
            # vol1, vol2 = bayesian_optimizer.suggest_new_parameters(vol1, vol2, corrosion_current)

            steps += 1

        # Return the final DataFrame
        return self.data

    def save_to_excel(self, file_name="experiment_data.xlsx"):
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, file_name)
        self.data.to_excel(file_path, index=False)
        print(f"Data saved to {file_path}")


runfile = BackendExperiment()
# runfile.add_volumes('AB', 20, 'CD', 20)
# runfile.save_to_excel(file_name="experiment_data.xlsx")
