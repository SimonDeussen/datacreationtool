from os import getcwd
from os.path import isfile, join
from os import listdir


import multiprocessing
from functools import partial

import numpy as np

NUM_OF_PROCESSES = 8
import imgkit

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("folder_path_html", help="enter the path to the folder with tokens") 
parser.add_argument("folder_path_out", help="enter the path to the folder with tokens") 

args = parser.parse_args()

FILE_TYPE = ".jpg"

def createScreenshots():
    path =  args.folder_path_html
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    indexes = range(NUM_OF_PROCESSES)
    splitted_files = np.array_split(onlyfiles, NUM_OF_PROCESSES)

    pool = multiprocessing.Pool(processes=NUM_OF_PROCESSES)
    func = partial(createScreenshotFromHtmlFile, splitted_files)
    pool.map(func, indexes)

def createScreenshotFromHtmlFile(fileNames, index):
    for filename in fileNames[index]:
        print(filename)
        file_out = filename.replace(".html", "")
        try:
            imgkit.from_file(args.folder_path_html + filename, args.folder_path_out + file_out + FILE_TYPE)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    createScreenshots()