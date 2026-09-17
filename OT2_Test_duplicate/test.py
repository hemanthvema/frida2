from Minerva_Lite import *


if __name__ == '__main__':
    # Reload the last configuration
    Configuration.load_configuration()
    
    # Rebind the objects that were loaded to variables
    ot2 = Configuration.OpentronsOT2["ot2"]
    # new_container = Container(0, 3, 1, 'New_Container_for_Testing', '100.0 mL', '120.0 mL', None, False, False)

    # new_inhibtor = Configuration.register_object(new_container)
    corrosion_inhibitor1_container = Configuration.Containers['corrosion_inhibitor1_container']
    corrosion_inhibitor2_container = Configuration.Containers['corrosion_inhibitor2_container']
    target_container = Configuration.Containers['target_container']

    # Define the chemicals that are added (giving the volumes and containers of the stock solutions)
    inhibitor1_vol = 10 
    inhibitor2_vol = 20 
    steps = 0
    maximum_steps = 50
    corrosion_current = 10
    target_corrosion_current = 0.01
    vol1 = 20.0
    vol2 = 20.0

    while (corrosion_current > target_corrosion_current and steps < maximum_steps):
        corrosion_inhibitor1 = Chemical(container=corrosion_inhibitor1_container, volume=f'{vol1} uL', name='CorrosionInhibitor1')
        corrosion_inhibitor2 = Chemical(container=corrosion_inhibitor2_container, volume=f'{vol2} uL', name='CorrosionInhibitor2')
        # Perform the addition step    
        ot2.add(chemical=[corrosion_inhibitor1, corrosion_inhibitor2], target_container=target_container)

        corrosion_current = electrochemistry.measure()
        vol1, vol2 = bayesian_optimizer.suggest_new_parameters(vol1, vol2, corrosion_current)
        
        steps += 1