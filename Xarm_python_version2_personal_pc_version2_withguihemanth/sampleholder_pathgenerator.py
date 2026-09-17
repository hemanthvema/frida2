import copy

class PathGenerator:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.paths = {
    'row1_col1': [[ 87,   177.2, 154.2, 180, 0, 0],            #constant
                    [-56.9, 177.2, 154.2, 180, 0, 0],          #constant
                    [-56.9, 177.2, 154.2, 153.8, -86, 115.6],  #constant
                    [-52.2, 177.2, 110 , 153.8, -86, 115.6], #changes in x directi
                    [-52.2, 220, 110, 153.8, -86, 115.6], # changes in y direction
                    # gripper closes and lifting the changes in z direction 
                    [-52.2, 220, 450, 153.8, -86, 115.6], # changes in z direction 

       ],
    'row1_col2': [[ 87,   177.2, 154.2, 180, 0, 0],            #constant
                    [-56.9, 177.2, 154.2, 180, 0, 0],          #constant
                    [-56.9, 177.2, 154.2, 153.8, -86, 115.6],  #constant
                    [ 11.2, 177.2, 110, 153.8, -86, 115.6], #changes in x directi
                    [ 11.2, 220, 110, 153.8, -86, 115.6],  #changes in y direction
                    [ 11.2, 220, 450, 153.8, -86, 115.6],], # changes in z direction
                    


    'row2_col1': [  [ 87,   177.2, 154.2, 180, 0, 0],            #constant
                    [-56.9, 177.2, 154.2, 180, 0, 0],          #constant
                    [-56.9, 177.2, 154.2, 153.8, -86, 115.6],  #constant
                    [-21.2, 177.2, 110, 153.8, -86, 115.6], #changes in x directi
                    [-21.2, 237.4, 110, 153.8, -86, 115.6], # changes in y direction
                    # gripper closes and lifting the changes in z direction 
                    [-21.2, 237.4, 450, 153.8, -86, 115.6], # changes in z direction 

       ],
    'row2_col2': [  [ 87,   177.2, 154.2, 180, 0, 0],            #constant
                    [-56.9, 177.2, 154.2, 180, 0, 0],          #constant
                    [-56.9, 177.2, 154.2, 153.8, -86, 115.6],  #constant
                    [ 39.2, 177.2, 110, 153.8, -86, 115.6], #changes in x directi
                    [ 39.2, 237.4, 110, 153.8, -86, 115.6],  #changes in y direction
                    [ 39.2, 237.4, 450,   153.8, -86, 115.6],], # changes in z direction
                    
                  }
        self.paths_remainings = {}
        self.constant_path = []

        self.x = -52.2
        self.x2 = 11.2
        self.y = 220
        self.y2 = 220
        self.z = 110
        self.z2 = 450
        self.y_increment_odd = 36
        self.x_increment_odd = 63.4

        self.x1_even = -21.2
        self.x2_even = 39.2
        self.y_even = 237.4
        self.y2_even = 237.4
        self.y_increment_even = 36
        self.x_increment_even = 60.4

        self.constant_path = self.paths['row1_col1'][:3]
                              
                              

    def generate_paths(self):
        #self.generate_constant_paths()
        self.generate_remaining_paths()
        self.paths.update(self.paths_remainings)

#     def generate_constant_paths(self):
#         for row in range(1, self.rows + 1):
#             for col in range(1, self.columns + 1):
#                 self.paths[f'row{row}_col{col}'] = copy.deepcopy(self.constant_path)

    def generate_remaining_paths(self):
        for row in range(1, self.rows + 1):
            for col in range(1, self.columns + 1):
                if row > 1 and col == 1:
                    if row % 2 == 1:
                        self.generate_odd_row_column1(row, col)
                    elif row != 2 and row % 2 == 0:
                        self.generate_even_row_column1(row, col)
                elif row > 1 and col == 2:
                    if row % 2 == 1:
                        self.generate_odd_row_column2(row, col)
                    elif row != 2 and row % 2 == 0:
                        self.generate_even_row_column2(row, col)

    def generate_odd_row_column1(self, row, col):
        self.paths_remainings[f'row{row}_col{col}'] = copy.deepcopy(self.constant_path)
        self.paths_remainings[f'row{row}_col{col}'].append([self.x] +
                                                           [self.paths_remainings[f'row{row}_col{col}'][2][1]] +
                                                           [self.z] +
                                                           self.paths_remainings[f'row{row}_col{col}'][2][3:])
        self.y += self.y_increment_odd
        self.paths_remainings[f'row{row}_col{col}'].append([self.x] + [self.y] +
                                                           self.paths_remainings[f'row{row}_col{col}'][3][2:])
        self.paths_remainings[f'row{row}_col{col}'].append([self.x] + [self.y] + [self.z2] +
                                                           self.paths_remainings[f'row{row}_col{col}'][4][3:])

    def generate_even_row_column1(self, row, col):
        self.paths_remainings[f'row{row}_col{col}'] = copy.deepcopy(self.constant_path)
        self.paths_remainings[f'row{row}_col{col}'].append([self.x1_even] +
                                                           [self.paths_remainings[f'row{row}_col{col}'][2][1]] +
                                                           [self.z] +
                                                           self.paths_remainings[f'row{row}_col{col}'][2][3:])
        self.y_even += self.y_increment_even
        self.paths_remainings[f'row{row}_col{col}'].append([self.x1_even] + [self.y_even] +
                                                           self.paths_remainings[f'row{row}_col{col}'][3][2:])
        self.paths_remainings[f'row{row}_col{col}'].append([self.x1_even] + [self.y_even] + [self.z2] +
                                                           self.paths_remainings[f'row{row}_col{col}'][4][3:])

    def generate_odd_row_column2(self, row, col):
        self.paths_remainings[f'row{row}_col{col}'] = copy.deepcopy(self.constant_path)
        self.paths_remainings[f'row{row}_col{col}'].append([self.x2] +
                                                           [self.paths_remainings[f'row{row}_col{col}'][2][1]] +
                                                           [self.z] +
                                                           self.paths_remainings[f'row{row}_col{col}'][2][3:])
        self.y2 += self.y_increment_odd
        self.paths_remainings[f'row{row}_col{col}'].append([self.x2] + [self.y2] +
                                                           self.paths_remainings[f'row{row}_col{col}'][3][2:])
        self.paths_remainings[f'row{row}_col{col}'].append([self.x2] + [self.y2] + [self.z2] +
                                                           self.paths_remainings[f'row{row}_col{col}'][4][3:])

    def generate_even_row_column2(self, row, col):
        self.paths_remainings[f'row{row}_col{col}'] = copy.deepcopy(self.constant_path)
        self.paths_remainings[f'row{row}_col{col}'].append([self.x2_even] +
                                                           [self.paths_remainings[f'row{row}_col{col}'][2][1]] +
                                                           [self.z] +
                                                           self.paths_remainings[f'row{row}_col{col}'][2][3:])
        self.y2_even += self.y_increment_even
        self.paths_remainings[f'row{row}_col{col}'].append([self.x2_even] + [self.y2_even] +
                                                           self.paths_remainings[f'row{row}_col{col}'][3][2:])
        self.paths_remainings[f'row{row}_col{col}'].append([self.x2_even] + [self.y2_even] + [self.z2] +
                                                           self.paths_remainings[f'row{row}_col{col}'][4][3:])


path_generator = PathGenerator(rows=13, columns=2)
path_generator.generate_paths()
# for keys, values in path_generator.paths.items():
#     print(keys, values)
    
    
# def get_values():
#     keys = list(path_generator.paths.keys())
    
#     for position in range(len(keys)):
        
#         key = keys[position]
#         values = path_generator.paths[key]
        
#         print(f"value for key '{key}:")
        
#         for value in values:
#             print(values)
     

# # Example usage
# get_values()