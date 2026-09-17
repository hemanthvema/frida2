
# import sampleholder_pathgenerator as sp


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


import sampleholder_pathgenerator as sp

def xarmpath(zero_position, paths, joint_motion_1, joint_motion_2, linear_motion_1, linear_motion_2):
    positions_sampleholder = list(sp.path_generator.paths.keys())
    
    for steps, position in enumerate(positions_sampleholder, start=1):
        print(f"Run {steps}:")
        print("zero position:", zero_position)
        print("position:", position)
        print("Path:")
        for point in sp.path_generator.paths[position]:
            print(point)
        print("Joint_motion 1:", joint_motion_1)
        print("Joint_motion 2:", joint_motion_2)
        print("Linear motion constant 1:", linear_motion_1)
        print("Linear motion constant 2:", linear_motion_2)
        print("zero position:", zero_position)

zero_position = [0, 0, 0, 0, 0, 0]
paths = sp.path_generator.paths
joint_motion_1 = [1, 2, 1, 2, 112, 1, 2, 2, 45]
joint_motion_2 = [1, 2, 1, 2, 112, 1, 2, 2, 45]
linear_motion_1 = [10, 20, 30, 40, 50, 60]
linear_motion_2 = [10, 20, 30, 40, 50, 60]

xarmpath(zero_position, paths, joint_motion_1, joint_motion_2, linear_motion_1, linear_motion_2)

