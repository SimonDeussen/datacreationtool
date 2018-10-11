from assets.Element import *
from assets.TokenBuilder import *

import json
from os import getcwd
from os.path import isfile, join
from os import listdir
import numpy as np

import time
import imgkit


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("file_path", help="enter the path to the sampled gui file")


args = parser.parse_args()

if args.file_path == "":
    print("Error: not enough argument supplied:")
    print("enter a path with a file to converse")
    exit(0)
    
tokenBuilder = TokenBuilder()

current_milli_time = lambda: int(round(time.time() * 1000))

def getTokenListFromFile(filepath):
    with open(filepath) as data_file:
        tokenString = data_file.read()
    
    cleaned = tokenString.replace("},", "}")
    cleaned = cleaned.replace("{", " {")

    print(cleaned)
    raw = cleaned.split("\n")

    splitted_elements = []
    for raw_element in raw:
        if len(raw_element) > 0:        
            if raw_element.find(" ") > -1:
                elements = raw_element.split(" ")
                splitted_elements.extend(elements)
            elif raw_element.find(",") > -1:
                elements = raw_element.split(",")
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


def saveHtmlToFileFromLayout(rootNode, dsl_mapping):
    file_name = "sampled_generation" + "_" + time.strftime("%d.%m.%Y") + "_" + str(current_milli_time())

    file_html =  open("generatedMarkup/" + file_name  + ".html","w+")
    file_html.write(rootNode.render(dsl_mapping))

    return file_name
   


if __name__ == '__main__':
    with open("assets/dsl-mapping.json") as data_file:
        dsl_mapping = json.load(data_file)


    token_list = getTokenListFromFile(args.file_path)
    rootNode = createElementsFromTokenList(token_list)
    file_name = saveHtmlToFileFromLayout(rootNode, dsl_mapping)

    imgkit.from_file("generatedMarkup/" + file_name + ".html" , 'generatedMarkup/' + file_name + '.png')
    print("generated html + img successfully:", file_name)

