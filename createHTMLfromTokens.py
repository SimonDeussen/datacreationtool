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


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("folder_path", help="enter the path to the folder with tokens") 
parser.add_argument("folder_path_out", help="enter the path to the folder with tokens") 

args = parser.parse_args()

if args.folder_path == "" or args.folder_path_out == "":
    print("Error: not enough argument supplied:")
    print("enter a path with a file to converse")
    exit(0)

token_counts = []
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
    
    token_counts.append(len(processed))
    return processed

def createNewContentElement(tag_name):
    content = ""

    if tag_name in ["single", "double", "quadruple"]:
        content = ""
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
    path =  args.folder_path
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and f != ".gitignore"]

    all_compiled_layouts = []

    for file in tqdm(onlyfiles):
        token_list = getTokenListFromFile(path + file)
        try:
            rootNode = createElementsFromTokenList(token_list)
        except Exception as ex:
            print(ex)
            print("errpor in file:", file)
        
        entry = {"file_name": file, "rootNode": rootNode }
        all_compiled_layouts.append(entry)

    print("read and compiled", len(all_compiled_layouts), "token lists from", path + "*")

    return all_compiled_layouts

def saveHtmlToFileFromLayout(entry, dsl_mapping):
    file_name = entry["file_name"].replace(".gui", "")
    file_html =  open( args.folder_path_out + file_name  + ".html","w+")
    file_html.write(entry["rootNode"].render(dsl_mapping))

    return True

def handleMPHtmlFileCreation(list, dsl_mapping, startIndex):
    for i in tqdm(range(len(list[startIndex]))):
        saveHtmlToFileFromLayout(list[startIndex][i], dsl_mapping)
    

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


    print("Token length analysis:")
    print("     average token length:", sum(token_counts)/float(len(token_counts)))
    print("     max token length:    ", max(token_counts))
    print("     min token length:    ", min(token_counts))
    token_counts.sort()
    print("     median token length: ", token_counts[int(len(token_counts)/2)])
