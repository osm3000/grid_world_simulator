import numpy as np
class map_parser:
    def __init__(self, map_path="./maps/TestMap_1"):
        self.map_path = map_path
        self.map_matrix = None
        self.dictionary = None
        self.empty = None
        self.subgoals = None # All numbers from 0 to 9
        self.eligible_space = None
        self.unique_elements = None
        self.map_unique_elements = {}

    def read_map(self):
        self.map_matrix = []
        with open(self.map_path, 'r') as fileHandle:
            lines = fileHandle.read().splitlines()
            for line in lines:
                self.map_matrix.append(list(line))
        self.map_matrix = np.array(self.map_matrix)
        self.unique_elements = np.unique(self.map_matrix)
        for element_index, element in enumerate(self.unique_elements):
            self.map_unique_elements[element] = element_index
        return self.map_matrix

    def extract_empty(self):
        self.empty = self.map_matrix == ' '
        self.empty = np.transpose(self.empty.nonzero())
        return self.empty

    def eligible_space(self):
        self.eligible_space = self.map_matrix != '#'
        self.eligible_space = np.transpose(self.empty.nonzero())
        return self.eligible_space

    def map_symbol(self, symbol):
        return self.map_unique_elements[symbol]

# parser = map_parser()
# parser.read_map()
# for item in parser.map_matrix:
#     print (item)
# print (parser.map_matrix.shape)
# print (parser.unique_elements)
# print (parser.map_unique_elements)
# parser.extract_empty()
# print (parser.empty.shape)
