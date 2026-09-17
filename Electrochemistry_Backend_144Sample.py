import serial
import time
import re
#import pump_official
import plot_cv
import plot_ocp
import plot_chronoamperometry
import os
import datetime

class Ender3_printer:
    def __init__(self, name, port_num, default_X, default_Y, default_Z):
        self.name = name
        self.port_num = port_num
        self.default_X = default_X
        self.default_Y = default_Y
        self.default_Z = default_Z
        self.connection = serial.Serial(port=self.port_num, baudrate=115200, timeout=1)
        
    def __str__(self):
        return f"The {self.name} is a Ender3 Pro printer connected to {self.port_num}, Default position is X:{default_X}, Y:{default_Y}, Z:{default_Z}"

    def send_cmd(self, cmd):
        # Sending a command to the printer and displaying the sent command.
        self.connection.write(f"{cmd}\n".encode("ASCII"))
        print(f"{cmd} has been sent to the {self.name}")

    def heat_bed(self, temp):
        comm = "M190 " #Max: 110
        comm += f"S{temp}"
        self.send_cmd(comm)

    def move(self, x=None, y=None, z=None):
        # Creating G-Code for linear movement to a point. G0 Defines a linear non-extrustion (No E-axis) movement.

        comm = "G0"
        if x is not None:
            comm += f" X{x} "
        if y is not None:
            comm += f" Y{y} "
        if z is not None:
            comm += f" Z{z} "

        comm+= "F5000" 
        # F sets the speed as mm/min
        self.send_cmd(comm)


    def move_relative(self, x=None, y=None, z=None):
        # Creating G-Code for linear movement taking x, y, z as relative amounts.
        self.send_cmd("G91")
        self.move(x,y,z)

    def move_absolute(self, x=None, y=None, z=None):
        # Creating G-Code for linear movement taking x, y, z as absolute amounts.
        self.send_cmd("G90")
        self.move(x,y,z)

    def autohome(self):
        # The printer goes to X, Y, Z = 0
        self.send_cmd("G28")
    
    def default(self):
        self.move_absolute(x=self.default_X, y=self.default_Y, z=self.default_Z)

    # '''def get_position(self):
    #     self.send_cmd("M114")
        
    #     response = self.connection.readline().decode()
    #     print(f'printer says {response}')
    #     match = re.findall(r"[-+]?\d*\.\d+|\d+", response)
    #     print (match)
    #     if len(match) < 3:
    #         print("Not enough match found in the response")
            
    #         return None
    #     else:
    #     # Save the first x, y, z values in a list
    #         xyz_values = [float(match[0]), float(match[1]), float(match[2])]
    #         print(match)
    #         print(xyz_values)
    #         return xyz_values

    # def wait_until_position(self, expected_X, expected_Y, expected_Z):
    #     xyz_values = self.get_position()
    #     expected_pos = [float(expected_X), float(expected_Y), float(expected_Z)]
    #     print(expected_pos)
    #     print(xyz_values)
    #     while xyz_values != expected_pos:
    #         print('Waiting')
    #         print(xyz_values)
    #         time.sleep(1)
    #     print('go')'''

    #def Measurement(self, zheight, flow_rate, flow_time, rinse_time, measurement_channel, rinse_channel, step_text_final, samples_list):
    def Measurement(self, zheight, step_text_final , samples_list):


        # Create a dict with sample number and coordinations
        samples_dict = {}
        sample_spacing = 10

        for i in range(1, 145):
            x = (i - 1) % 12
            y = (i - 1) // 12
            samples_dict[i] = [x, y]

        cord_dict = {}
        for sample in range(1,145):
            cord_x = 50 + (samples_dict[sample][0] * sample_spacing)
            cord_y = 50 + (samples_dict[sample][1] * sample_spacing)
            cord_dict[sample] = [cord_x,cord_y]

        for sample_num in samples_list:

            #Create a folder to save the data of each experiment in
            current_time = datetime.datetime.now().strftime("%d.%m.%Y-%H.%M")
            base_path = "Results"
            folder_name = "Experiment_" + current_time + '_Sample position_' + str(sample_num)
            folder_path = os.path.join(base_path, folder_name)
            os.makedirs(folder_path)

            print (f"Experiment started on sample position {sample_num} on {cord_dict[sample_num]}")

            # Start the pump and fill the liquid
            #pump_official.pump_obj.set_runtime(float(flow_rate), int(flow_time), units= 's', chan = measurement_channel)
            #time.sleep(flow_time+5)


            for step in step_text_final:
                # Move the printer to sample position.
                x_sample = cord_dict[sample_num][0]
                y_sample = cord_dict[sample_num][1]
                self.move_absolute(x = x_sample, y = y_sample, z=zheight)
                time.sleep(15)


                #Do the measurement

                #For each step do the correct measurement and save the data
                if step == "Cyclic Voltammetry":
                    print('CV measurement started')
                    plot_cv.emstat_cv(folder_path)
            
            
                elif step == "Open Circuit Potential":
                    print('OCP measurement started')
                    plot_ocp.emstat_ocp(folder_path)
                
                elif step == "Chronoamperometry":
                    print('Chronoamperometry measurement started')
                    plot_chronoamperometry.emstat_chronoamperometry(folder_path)
                
            #Start the pump to rinse
            #pump_official.pump_obj.set_runtime(float(flow_rate), int(rinse_time), units= 's', chan = rinse_channel)
            #time.sleep(rinse_time+5)
            time.sleep(20)

            
        
# Defining the name, port and the default resting position for printer.
electrochem_port = "COM18"

default_X = 50  
default_Y = 50
default_Z = 90
electrochem = Ender3_printer("Electrochemistry Unit", electrochem_port, default_X, default_Y, default_Z)
electrochem.move_absolute(None,None,144)
