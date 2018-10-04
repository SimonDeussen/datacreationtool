from os import getcwd
from os.path import isfile, join
from os import listdir

from tqdm import tqdm

import multiprocessing
from functools import partial

import numpy as np

NUM_OF_PROCESSES = 4
import imgkit

def createScreenshots():
    path =  getcwd() + "/markup/"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    indexes = range(NUM_OF_PROCESSES)
    splitted_files = np.array_split(onlyfiles, NUM_OF_PROCESSES)

    pool = multiprocessing.Pool(processes=NUM_OF_PROCESSES)
    func = partial(createScreenshotFromHtmlFile, splitted_files)
    pool.map(func, indexes)

def createScreenshotFromHtmlFile(fileNames, index):
    for filename in fileNames[index]:
        print(filename)
        try:
            imgkit.from_file("markup/" + filename, 'img/' + filename + '.jpg')
        except Exception as e:
            print(e)

if __name__ == '__main__':
    createScreenshots()