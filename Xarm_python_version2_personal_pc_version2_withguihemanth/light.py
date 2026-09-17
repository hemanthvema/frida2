from opentrons import protocols, robot

def turn_on_lights():
    # Code to turn on lights
    pass

def turn_off_lights():
    # Code to turn off lights
    pass

if robot.is_simulating():
    # If the robot is running in simulation mode
    turn_on_lights()
else:
    # If the robot is running on the physical OT-2
    if robot.is_connected():
        turn_on_lights()
        protocol = protocols.load('your_protocol.py')
        protocol.run()
        turn_off_lights()
    else:
        turn_off_lights()
