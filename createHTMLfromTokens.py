from assets.Element import *
from assets.TokenBuilder import *
import json
from os import getcwd
from os.path import isfile, join
from os import listdir

import time
from tqdm import tqdm

import multiprocessing
from functools import partial

import numpy as np

tokenBuilder = TokenBuilder()

NUM_OF_PROCESSES = 4

current_milli_time = lambda: int(round(time.time() * 1000))

def getTokenListFromFile(filepath):
    with open(filepath) as data_file:
        tokenString = data_file.read()
    
    raw = tokenString.split("\n")

    splitted_elements = []
    for raw_element in raw:
        if len(raw_element) > 0:        
            if raw_element.find(" ") > -1:
                elements = raw_element.split(" ")
                splitted_elements.extend(elements)
            else:
                splitted_elements.append(raw_element)     

    processed = []
    for element in splitted_elements:
        if element != "":
            if element.find(",") > -1:
                element = element.replace(",", "")

            processed.append(element)
    
    return processed

def createNewContentElement(tag_name):
    content = ""

    if tag_name in ["single", "double"]:
        content = "" #tokenBuilder.createRandomParagraphText()
    elif tag_name in ["text"]:
        content = tokenBuilder.createRandomShortParagraphText()
    elif tag_name in ["sidebar-element", "btn-inactive-blue", "btn-inactive-black", "btn-inactive-grey", "btn-inactive-white"]:
        content = tokenBuilder.createRandomMenuItemText()
    elif tag_name in ["small-title"]:
        content = tokenBuilder.createRandomHeadlineText()


    return Element(tag_name, content)
def createElementsFromTokenList(token_list):
    token_list.reverse()

    root = Element(token_list.pop(), "")
    parentStack = []

    lastElement = root

    while len(token_list) > 0:

        if token_list[-1] == "{":
            parentStack.append(lastElement)
            token_list.pop()

        elif token_list[-1] == "}":
            parentStack.pop()
            token_list.pop()

        else:
            new_element = createNewContentElement(token_list.pop())
            parentStack[-1].addChildren(new_element)
            lastElement = new_element

    return root

def readAllTokensAndCompile():
    path =  getcwd() + "/token/"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and f != ".gitignore"]

    all_compiled_layouts = []

    for file in tqdm(onlyfiles):
        token_list = getTokenListFromFile(path + file)
        try:
            rootNode = createElementsFromTokenList(token_list)
        except Exception as ex:
            print(ex)
            print("errpor in file:", file)
        all_compiled_layouts.append(rootNode)

    print("read and compiled", len(all_compiled_layouts), "token lists from", path + "*")

    return all_compiled_layouts

def saveHtmlToFileFromLayout(rootNode, index, dsl_mapping):
    filename = "complete_generation" + "_" + str(index) + "_" + time.strftime("%d.%m.%Y") + "_" + str(current_milli_time())

    file_html =  open("markup/" + filename  + ".html","w+")
    file_html.write(rootNode.render(dsl_mapping))

    file_token = open("token/" + filename + ".gui", "w+")
    file_token.write(rootNode.toString2())

    return True

def handleMPHtmlFileCreation(list, dsl_mapping, startIndex):
    for i in tqdm(range(len(list[startIndex]))):
        file_index = i + startIndex*NUM_OF_PROCESSES
        saveHtmlToFileFromLayout(list[startIndex][i], file_index, dsl_mapping)
    

def createHtml(layouts):
    with open("assets/dsl-mapping.json") as data_file:
        dsl_mapping = json.load(data_file)
        
    indexes = range(NUM_OF_PROCESSES)
    splitted_layouts = np.array_split(layouts, NUM_OF_PROCESSES)

    pool = multiprocessing.Pool(processes=NUM_OF_PROCESSES)
    func = partial(handleMPHtmlFileCreation, splitted_layouts, dsl_mapping)
    pool.map(func, indexes)


if __name__ == '__main__':
    all_layouts = readAllTokensAndCompile()
    createHtml(all_layouts)
