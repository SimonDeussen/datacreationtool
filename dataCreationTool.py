import time
import json
import imgkit
import random
import itertools

import numpy as np

from os import getcwd
from os import listdir

import multiprocessing
from functools import partial

from os.path import isfile, join

from assets.TokenBuilder import *
from assets.Element import *

NUM_OF_PROCESSES = 16

tokenBuilder = TokenBuilder()

current_milli_time = lambda: int(round(time.time() * 1000))

def createRandomFile():
    with open("assets/dsl-mapping.json") as data_file:
        dsl_mapping = json.load(data_file)

    root = Element("body", "")

    menue_or_sidebar = random.choice([True, False])

    if menue_or_sidebar:
        logo_left = random.choice([True, False])
        num_of_menue_buttons = random.randint(1,4)

        menu = tokenBuilder.createMenu(logo_left, num_of_menue_buttons)
        root.addChildren(menu)
    else:
        sidebar = tokenBuilder.createSidebar(4)
        root.addChildren(sidebar)

    num_of_rows = random.randint(1,3)

    for i in range(num_of_rows):
        row_type = random.randint(0,4)
        row = tokenBuilder.createRow(row_type)
        print("adding row", i, "of total", num_of_rows)
        root.addChildren(row)

    filename = "random_generation" + "_" + time.strftime("%d.%m.%Y-%H:%M:%S")

    file_html =  open("markup/" + filename  + ".html","w+")
    file_token = open("token/" + filename + ".gui", "w+")

    token_sequence = root.toString2()
    file_token.write(token_sequence)
    
    html = root.render(dsl_mapping)
    file_html.write(html)

    return filename

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

    print("created", len(complete_layouts), "different layouts")

    return complete_layouts

def handleMPHtmlFileCreation(list, dsl_mapping, startIndex):
    for i in range(len(list[startIndex])):
        file_index = i + startIndex*NUM_OF_PROCESSES

        print("process", startIndex, "creating html file", i, file_index )
        saveHtmlToFileFromLayout(list[startIndex][i], file_index, dsl_mapping)
    

def saveHtmlToFileFromLayout(rootNode, index, dsl_mapping):
    filename = "complete_generation" + "_" + str(index) + "_" + time.strftime("%d.%m.%Y") + "_" + str(current_milli_time())

    file_html =  open("markup/" + filename  + ".html","w+")
    file_html.write(rootNode.render(dsl_mapping))

    file_token = open("token/" + filename + ".gui", "w+")
    file_token.write(rootNode.toString2())

    return True


def createScreenshotFromHtmlFile(fileNames, index):
    for filename in fileNames[index]:
        print(filename)
        try:
            imgkit.from_file("markup/" + filename, 'img/' + filename + '.jpg')
        except Exception as e:
            print(e)

def createHtml():
    complete_layouts = createAllPossibilities()
    print(len(complete_layouts))
    with open("assets/dsl-mapping.json") as data_file:
        dsl_mapping = json.load(data_file)
        
    indexes = range(NUM_OF_PROCESSES)
    splitted_layouts = np.array_split(complete_layouts, NUM_OF_PROCESSES)

    pool = multiprocessing.Pool(processes=NUM_OF_PROCESSES)
    func = partial(handleMPHtmlFileCreation, splitted_layouts, dsl_mapping)
    pool.map(func, indexes)


def createScreenshots():
    path =  getcwd() + "/markup/"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    indexes = range(NUM_OF_PROCESSES)
    splitted_files = np.array_split(onlyfiles, NUM_OF_PROCESSES)

    pool = multiprocessing.Pool(processes=NUM_OF_PROCESSES)
    func = partial(createScreenshotFromHtmlFile, splitted_files)
    pool.map(func, indexes)


# def compileTokenSequence(tokenString):


if __name__ == '__main__':
    createHtml()
    # createScreenshots()


    
    
    
