import sampleholder_pathgenerator as sp
import sys
import math
import time
import queue
import datetime
import random
import traceback
import threading
from xarm import version
import xarm
from xarm.wrapper import XArmAPI

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
    def run(self, zero_position = None, paths = None, num_samples = None,  joint_motion_1 = None, joint_motion_2= None , linear_motion_1= None, linear_motion_2 = None ):

        try:
            self._arm.reset()
            time.sleep(1)

            positions_sampleholder = list(sp.path_generator.paths.keys())

            for steps, position in enumerate(positions_sampleholder, start = 1):

                print(f"sample {steps}:")
                print("zero position:", zero_position)

                time.sleep(1)
                code = self._arm.set_position(*zero_position, speed=100, mvacc=100, radius=0.0, wait=True)
                if code != 0:
                    print("Error occurred while setting zero position")
                    return
                #print("position:", position)
                print("Path:")


                for index, point in enumerate(sp.path_generator.paths[position], start =1):
                    print(point)
                    time.sleep(1)
                    code = self._arm.set_position(*point, speed=100, mvacc=100, radius=0.0, wait=True )

                    if index == 5:
                        time.sleep(5)
                        code = self._arm.close_lite6_gripper()
                        time.sleep(5)
                        if  code!= 0:
                            print("Error occured while closing the gripper")
                            return


                    time.sleep(5)
                #print("Path:", self.paths[position])

                time.sleep(1)
                code = self._arm.set_servo_angle(angle=[-82.0, -22.3, 52.7, -151.7, 17.4, 150.7], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                time.sleep(1)

                code = self._arm.set_servo_angle(angle=[-96.6, 3.5, 75.0, -199.1, 19.9, 196.1], speed=self._angle_speed, mvacc=self._angle_acc, wait=True, radius=0.0)
                if not self._check_code(code, 'set_servo_angle'):
                    return
                time.sleep(1)

                code = self._arm.set_position(*[-29.3, -316.3, 333.0, 78.4, -87.9, 11.5], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                time.sleep(1)

                code = self._arm.open_lite6_gripper()
                time.sleep(5)
                self._arm.stop_lite6_gripper()
                time.sleep(1)
                if not self._check_code(code, 'open_lite6_gripper'):
                    return
                
                time.sleep(5)


                        
                code = self._arm.set_position(*[-29.3, -316.3, 478.9, 78.4, -87.9, 11.5], speed=self._tcp_speed, mvacc=self._tcp_acc, radius=0.0, wait=True)
                if not self._check_code(code, 'set_position'):
                    return
                time.sleep(1)
                self._arm.reset()

                if steps >= num_samples:
                    break


                                        
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
    #robot_main.run(zero_position=[87, 0, 154.2, 180, 0, 0])
    robot_main.run(zero_position=[87, 0, 154.2, 180, 0, 0], paths = sp.path_generator.paths, num_samples = 2)










# def xarmpath(zero_position, paths, joint_motion_1, joint_motion_2, linear_motion_1, linear_motion_2):
    
#     positions_sampleholder =  list(sp.path_generator.paths.keys())
    
    
#     for steps, position in enumerate(positions_sampleholder, start =1):
        
#         print(f"Run {steps}:")
#         print("zero position:", zero_position)
#         print("position :", position)
#         print("Path:", sp.path_generator.paths[position])
#         print("Joint_motion 1:", joint_motion_1)
#         print("Joint_motion :", joint_motion_2)
#         print("Linear motion constant 1", linear_motion_1)
#         print("Linear motion constant 2", linear_motion_2)
#         print("zero position:", zero_position)
        
        
# zero_position = [0,0,0,00,0,0]
# paths = sp.path_generator.paths
# joint_motion_1 = [1,2,1,2,112,1,2,2,45]
# joint_motion_2 = [1,2,1,2,112,1,2,2,45]
# linear_motion_1 = [10,20,30,40,50,60]
# linear_motion_2 = [10,20,30,40,50,60]


# xarmpath(zero_position, paths, joint_motion_1, joint_motion_2, linear_motion_1, linear_motion_2)       

    

        
        
        
    










