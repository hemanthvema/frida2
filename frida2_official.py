#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
# Notice
#   1. Changes to this file on Studio will not be preserved
#   2. The next conversion will overwrite the file with the same name
# 
# xArm-Python-SDK: https://github.com/xArm-Developer/xArm-Python-SDK
#   1. git clone git@github.com:xArm-Developer/xArm-Python-SDK.git
#   2. cd xArm-Python-SDK
#   3. python setup.py install
"""
import sys
import os
import math
import time
import queue
import datetime
import random
import traceback
import threading

# # Get the current script's directory
# script_dir = os.path.dirname(os.path.abspath(__file__))
# # Append the parent directory of xarm_python to the Python path
# xarm_python_path = os.path.join(script_dir, 'Xarm_python_version2_personal_pc_version2_withguihemanth')
# #xarm_python_path = os.path.join(script_dir, 'electrochemistry_dupmergedfile')
# sys.path.append(xarm_python_path)

# # Add the parent directory to the Python path
# parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(parent_directory)

#import Xarm_python_version2_personal_pc_version2_withguihemanth.xarm

# Add the path of the Minerva_Lite module to the Python path
minerva_lite_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'OT2_Test_duplicate')
sys.path.append(minerva_lite_path)
import OT2_Test_duplicate.heyyounogui

import pump_official
import Xarm_python_version2_personal_pc_version2_withguihemanth.xarm.version as version
from Xarm_python_version2_personal_pc_version2_withguihemanth.xarm.wrapper import XArmAPI
import Electrochemistry_Backend_144Sample as electrochemistry


#import OT2_Test_duplicate 
#import OT2_Test_duplicate.heyyounogui 




class RobotMain(object):
    """Robot Main Class"""
    def __init__(self, robot, **kwargs):
        self.alive = True
        self._arm = robot
        self._tcp_speed = 100
        self._tcp_acc = 2000
        self._angle_speed = 20
        self._angle_acc = 500
        self._variables = {}
        self._robot_init()

    # Robot init
    def _robot_init(self):
        self._arm.clean_warn()
        self._arm.clean_error()
        self._arm.motion_enable(True)
        self._arm.set_mode(0)
        self._arm.set_state(0)
        time.sleep(1)
        self._arm.register_error_warn_changed_callback(self._error_warn_changed_callback)
        self._arm.register_state_changed_callback(self._state_changed_callback)
        if hasattr(self._arm, 'register_count_changed_callback'):
            self._arm.register_count_changed_callback(self._count_changed_callback)

    # Register error/warn changed callback
    def _error_warn_changed_callback(self, data):
        if data and data['error_code'] != 0:
            self.alive = False
            self.pprint('err={}, quit'.format(data['error_code']))
            self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)

    # Register state changed callback
    def _state_changed_callback(self, data):
        if data and data['state'] == 4:
            self.alive = False
            self.pprint('state=4, quit')
            self._arm.release_state_changed_callback(self._state_changed_callback)

    # Register count changed callback
    def _count_changed_callback(self, data):
        if self.is_alive:
            self.pprint('counter val: {}'.format(data['count']))

    def _check_code(self, code, label):
        if not self.is_alive or code != 0:
            self.alive = False
            ret1 = self._arm.get_state()
            ret2 = self._arm.get_err_warn_code()
            self.pprint('{}, code={}, connected={}, state={}, error={}, ret1={}. ret2={}'.format(label, code, self._arm.connected, self._arm.state, self._arm.error_code, ret1, ret2))
        return self.is_alive

    @staticmethod
    def pprint(*args, **kwargs):
        try:
            stack_tuple = traceback.extract_stack(limit=2)[0]
            print('[{}][{}] {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), stack_tuple[1], ' '.join(map(str, args))))
        except:
            print(*args, **kwargs)

    @property
    def is_alive(self):
        if self.alive and self._arm.connected and self._arm.error_code == 0:
            if self._arm.state == 5:
                cnt = 0
                while self._arm.state == 5 and cnt < 5:
                    cnt += 1
                    time.sleep(0.1)
            return self._arm.state < 4
        else:
            return False

    # Robot Main Run
    def run(self, num_samples = int, inlet_flow_rate = int, inlet_flow_time = int, inlet_measurement_channel = int, 
                                     outlet_flow_rate = int, outlet_flow_time = int, outlet_measurement_channel = int,
                                    inhibitor1 =str, vol1 =int , inhibitor2 = str, vol2 = int,
                                    zheight = int, step_text_final = list, samples_list = list):
        try:
            self._arm.reset() 
            time.sleep(1)
            code = self._arm.set_position(*[87.0, 177.2, 154.2, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
            if not self._check_code(code, 'set_position'):
                return
            time.sleep(1)
            code = self._arm.set_position(*[-56.9, 177.2, 154.2, 180.0, 0.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
            if not self._check_code(code, 'set_position'):
                return
            time.sleep(1)
            code = self._arm.set_position(*[-56.5, 177.2, 154.2, 153.8, -86.4, 115.6], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
            if not self._check_code(code, 'set_position'):
                return
            time.sleep(1)
            code = self._arm.set_position(*[-54.7, 177.2, 97.7, -180.0, -90.0, 90.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
            if not self._check_code(code, 'set_position'):
                return
            time.sleep(1)
            code = self._arm.set_position(*[-53.0, 230.8, 97.7, -180.0, -90.0, 90.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            time.sleep(5)
            code = self._arm.close_lite6_gripper()
            if not self._check_code(code, 'close_lite6_gripper'):
                return
            time.sleep(5)
            code = self._arm.set_position(*[-53.0, 230.8, 438.2, 0.0, -90.0, -90.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            time.sleep(1)
            code = self._arm.set_servo_angle(angle=[-82.0, -22.3, 52.7, -151.7, 17.4, 150.7], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            time.sleep(1)
            code = self._arm.set_servo_angle(angle=[-96.6, 3.5, 75.0, -199.1, 19.9, 196.1], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            time.sleep(1)
            code = self._arm.set_position(*[-29.6, -315.5, 453.6, 90.0, -90.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
            if not self._check_code(code, 'set_position'):
                return
            time.sleep(1)
            code = self._arm.set_position(*[-28.2, -329.7, 453.6, -90.0, -90.0, 180.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
            if not self._check_code(code, 'set_position'):
                return
            time.sleep(1)
            code = self._arm.set_position(*[-28.2, -329.7, 328.7, 90.0, -90.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
            if not self._check_code(code, 'set_position'):
                return
            time.sleep(5)
            code = self._arm.open_lite6_gripper()
            time.sleep(0.5)
            self._arm.stop_lite6_gripper()
            if not self._check_code(code, 'open_lite6_gripper'):
                return
            time.sleep(5)
            code = self._arm.set_position(*[-28.2, -329.7, 453.6, -90.0, -90.0, 180.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
            if not self._check_code(code, 'set_position'):
                return
            time.sleep(1)
            code = self._arm.set_servo_angle(angle=[0.0, 9.9, 31.8, 0.0, 21.9, 0.0], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
            if not self._check_code(code, 'set_servo_angle'):
                return
            time.sleep(10)
            for i in range(int(num_samples)):

                OT2_Test_duplicate.heyyounogui.runfile.add_volumes(inhibitor1, vol1, inhibitor2, vol2)
                time.sleep(10)
                if not self.is_alive: 
                    break
                code = self._arm.set_servo_angle(angle=[-96.0, 7.6, 79.5, -198.7, 19.0, 197.8], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                code = self._arm.set_position(*[-28.2, -329.7, 453.6, -90.0, -90.0, 180.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                time.sleep(1)
                code = self._arm.set_position(*[-28.2, -329.7, 328.7, 90.0, -90.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                time.sleep(5)
                code = self._arm.close_lite6_gripper()
                if not self._check_code(code, 'close_lite6_gripper'):
                    return
                time.sleep(5)
                code = self._arm.set_position(*[-28.2, -329.7, 453.6, -90.0, -90.0, 180.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                time.sleep(1)
                code = self._arm.set_servo_angle(angle=[-96.0, 7.6, 79.5, -198.7, 19.0, 197.8], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                code = self._arm.set_position(*[-28.2, -329.7, 453.6, -90.0, -90.0, 180.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                time.sleep(1)
                code = self._arm.set_servo_angle(angle=[-36.9, -41.0, 64.3, -198.3, -17.9, 198.4], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                time.sleep(3)
                code = self._arm.set_servo_angle(angle=[-21.0, -22.3, 27.3, -208.8, 37.1, 202.4], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                time.sleep(3)
                code = self._arm.set_servo_angle(angle=[-1.9, 7.3, 32.4, -182.0, 65.0, 180.9], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                
                #Inlet position. This is where the electrolyte will pump into the beaker
                code = self._arm.set_position(*[262.1, -6.5, 272.3, 90.0, -90.0, 90.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                
                time.sleep(10)

                code = self._arm.set_position(*[262.1, -6.5, 330.0, 90.0, -90.0, 90.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                time.sleep(10)
                
                #starting the pump to fill the beaker with electrolyte solution
                pump_official.pump_obj.set_runtime(float(inlet_flow_rate), int(inlet_flow_time), units= 's', chan = inlet_measurement_channel)
                time.sleep(10+ inlet_flow_time)



                code = self._arm.set_position(*[262.1, -6.5, 272.3, 90.0, -90.0, 90.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                time.sleep(3)



                code = self._arm.set_position(*[262.1, 76.0, 260, -90.0, -90.0, -90.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                time.sleep(2)
                code = self._arm.set_position(*[262.1, 76.0, 385.8, -90.0, -90.0, -90.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                time.sleep(10)

                #Outlet - start the pump to send the electrolyte solution and Inhibitor mix to the electrochemistry measurement department
                pump_official.pump_obj.set_runtime(float(outlet_flow_rate), int(outlet_flow_time), units= 's', chan = outlet_measurement_channel)
                time.sleep(10+ outlet_flow_time)

                #Measuring electrochemistry 
                time.sleep(20)
                electrochemistry.electrochem.Measurement(zheight, step_text_final, samples_list)


                code = self._arm.set_position(*[262.1, 76.0, 260, -90.0, -90.0, -90.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                time.sleep(5)
                code = self._arm.set_position(*[171.5, -198.0, 272.3, 90.0, -90.0, 90.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                time.sleep(2)
                code = self._arm.set_servo_angle(angle=[-34.1, 25.2, 95.1, -223.2, 25.9, 216.0], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                time.sleep(2)
                code = self._arm.set_servo_angle(angle=[-29.8, 30.1, 90.5, -228.5, 33.3, 92.1], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                time.sleep(5)
                code = self._arm.set_servo_angle(angle=[-30.6, 31.0, 90.4, -228.7, 41.8, 39.3], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                time.sleep(20)
                code = self._arm.set_servo_angle(angle=[-29.7, -53.8, 32.1, -265.4, 26.0, 267.0], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                for i in range(int(2)):
                    if not self.is_alive:
                        break
                    code = self._arm.set_servo_angle(angle=[-29.7, -53.8, 32.1, -265.4, 26.0, 267.0], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
                    if not self._check_code(code, 'set_servo_angle'):
                        return
                    time.sleep(2)
                    code = self._arm.set_servo_angle(angle=[-21.0, -22.3, 27.3, -208.8, 37.1, 202.4], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                    if not self._check_code(code, 'set_servo_angle'):
                        return
                    time.sleep(2)
                    code = self._arm.set_servo_angle(angle=[-1.9, 7.3, 32.4, -182.0, 65.0, 180.9], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                    if not self._check_code(code, 'set_servo_angle'):
                        return
                    code = self._arm.set_position(*[262.1, -6.5, 272.3, 90.0, -90.0, 90.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                    if not self._check_code(code, 'set_position'):
                        return
                    time.sleep(2)
                    code = self._arm.set_position(*[262.1, -6.5, 330.0, 90.0, -90.0, 90.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                    if not self._check_code(code, 'set_position'):
                        return
                    time.sleep(10)
                    code = self._arm.set_position(*[262.1, -6.5, 272.3, 90.0, -90.0, 90.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                    if not self._check_code(code, 'set_position'):
                        return
                    time.sleep(2)
                    code = self._arm.set_position(*[171.5, -198.0, 272.3, 90.0, -90.0, 90.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                    if not self._check_code(code, 'set_position'):
                        return
                    time.sleep(2)
                    code = self._arm.set_servo_angle(angle=[-34.1, 25.2, 95.1, -223.2, 25.9, 216.0], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                    if not self._check_code(code, 'set_servo_angle'):
                        return
                    time.sleep(2)
                    code = self._arm.set_servo_angle(angle=[-29.8, 30.1, 90.5, -228.5, 33.3, 92.1], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                    if not self._check_code(code, 'set_servo_angle'):
                        return
                    time.sleep(5)
                    code = self._arm.set_servo_angle(angle=[-30.6, 31.0, 90.4, -228.7, 41.8, 39.3], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                    if not self._check_code(code, 'set_servo_angle'):
                        return
                    time.sleep(20)
                    for i in range(int(5)):
                        if not self.is_alive:
                            break
                        code = self._arm.set_position(*[356.9, -152.3, 373.7, -92.7, 89.0, -93.3], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
                        if not self._check_code(code, 'set_position'):
                            return
                        code = self._arm.set_position(*[356.9, -152.3, 373.7, -92.7, 76.5, -93.3], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
                        if not self._check_code(code, 'set_position'):
                            return
                        code = self._arm.set_position(*[356.9, -172.4, 373.7, -92.7, 89.0, -93.3], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
                        if not self._check_code(code, 'set_position'):
                            return
                        code = self._arm.set_position(*[356.9, -172.4, 373.7, 87.3, 61.3, 86.7], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=False)
                        if not self._check_code(code, 'set_position'):
                            return
                time.sleep(2)
                code = self._arm.set_servo_angle(angle=[-34.1, 25.2, 95.1, -223.2, 25.9, 216.0], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                time.sleep(2)
                code = self._arm.set_servo_angle(angle=[-96.0, 7.6, 79.5, -198.7, 19.0, 197.8], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                time.sleep(2)
                code = self._arm.set_position(*[-28.2, -329.7, 453.6, -90.0, -90.0, 180.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                time.sleep(2)
                code = self._arm.set_position(*[-28.2, -329.7, 328.7, 90.0, -90.0, 0.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                time.sleep(5)
                code = self._arm.open_lite6_gripper()
                time.sleep(0.5)
                self._arm.stop_lite6_gripper()
                if not self._check_code(code, 'open_lite6_gripper'):
                    return
                time.sleep(5)
                code = self._arm.set_position(*[-28.2, -329.7, 453.6, -90.0, -90.0, 180.0], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                time.sleep(1)
                code = self._arm.set_servo_angle(angle=[0.0, 9.9, 31.8, 0.0, 21.9, 0.0], speed=self._angle_speed, mvacc=self._angle_acc, wait=False, radius=0.0)
                if not self._check_code(code, 'set_servo_angle'):
                    return
        except Exception as e:
            self.pprint('MainException: {}'.format(e))
        self.alive = False
        self._arm.release_error_warn_changed_callback(self._error_warn_changed_callback)
        self._arm.release_state_changed_callback(self._state_changed_callback)
        if hasattr(self._arm, 'release_count_changed_callback'):
            self._arm.release_count_changed_callback(self._count_changed_callback)


if __name__ == '__main__':
    RobotMain.pprint('xArm-Python-SDK Version:{}'.format(version.__version__))
    arm = XArmAPI('192.168.1.178', baud_checkset=False)
    robot_main = RobotMain(arm)
    robot_main.run(num_samples = 2, inlet_flow_rate = 25, inlet_flow_time = 60, inlet_measurement_channel = 1,
                   outlet_flow_rate = 25, outlet_flow_time = 80, outlet_measurement_channel = 3, 
                   inhibitor1 = 'Rashid', vol1 = 10 , inhibitor2 = 'Hemanth', vol2 = 10, 
                   zheight= 20, step_text_final= ["Cyclic Voltammetry", "Open Circuit Potential" , "Chronoamperometry"] , samples_list= [1] )
# RobotMain.pprint('xArm-Python-SDK Version:{}'.format(version.__version__))
# arm = XArmAPI('192.168.1.178', baud_checkset=False)
# robot_main = RobotMain(arm)

