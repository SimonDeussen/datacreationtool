import time
import json
import random
import itertools

import numpy as np

from os import getcwd
from os import listdir

import multiprocessing
from functools import partial


from assets.TokenBuilder import *
from assets.Element import *

from tqdm import tqdm
NUM_OF_PROCESSES = 1

tokenBuilder = TokenBuilder()

current_milli_time = lambda: int(round(time.time() * 1000))

def createAllPossibilities():
    menu_or_sidebar = [True, False]
    logo_left_or_right = [True, False]
    possible_num_of_menu_button = [1, 2, 3, 4]


    possible_num_of_rows = [1,2,3]
    possible_row_type = [0,1,2,3,4]

    row_count_layout_combinations = []

    for i in possible_num_of_rows:
        row_count_layout_combinations.extend( list(itertools.product(possible_row_type, repeat=i)))

    for i in range(len(row_count_layout_combinations)):
        row_count_layout_combinations[i] = list(row_count_layout_combinations[i])

    complete_layouts =  []

    for menu_flag in menu_or_sidebar:
        for logo_flag in logo_left_or_right:
            for num_of_menue_button in possible_num_of_menu_button:
                for row_count_layout in row_count_layout_combinations:

                        root = Element("body", "")

                        if menu_flag:
                            menu = tokenBuilder.createMenu(logo_flag, num_of_menue_button)
                            root.addChildren(menu)
                        else:
                            sidebar = tokenBuilder.createSidebar(num_of_menue_button)
                            root.addChildren(sidebar)

                        for i in range(len(row_count_layout)):
                            row = tokenBuilder.createRow(row_count_layout[i])
                            root.addChildren(row)

                        complete_layouts.append(root)

    print("Created", len(complete_layouts), "different layouts.")


    return complete_layouts


def saveTokenToFileFromLayout(rootNode, index, dsl_mapping):
    filename = "complete_generation" + "_" + str(index) + "_" + time.strftime("%d.%m.%Y") + "_" + str(current_milli_time())

    file_token = open("token/" + filename + ".gui", "w+")
    file_token.write(rootNode.toString2())
    return True


def handleTokenCreation(list, dsl_mapping, startIndex):
    for i in tqdm(range(len(list[startIndex]))):
        file_index = i + startIndex*NUM_OF_PROCESSES

        # print("process", startIndex, "creating token file", i, file_index )
        saveTokenToFileFromLayout(list[startIndex][i], file_index, dsl_mapping)
    
def createTokens():
    complete_layouts = createAllPossibilities()

    with open("assets/dsl-mapping.json") as data_file:
        dsl_mapping = json.load(data_file)
        
    indexes = range(NUM_OF_PROCESSES)
    splitted_layouts = np.array_split(complete_layouts, NUM_OF_PROCESSES)

    pool = multiprocessing.Pool(processes=NUM_OF_PROCESSES)
    func = partial(handleTokenCreation, splitted_layouts, dsl_mapping)
    pool.map(func, indexes)

if __name__ == '__main__':
    createTokens()


    
    