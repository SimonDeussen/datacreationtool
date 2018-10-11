import time
from os import listdir, makedirs
from os.path import isfile, join, exists
from random import shuffle
import argparse
from math import floor

from shutil import copy

from tqdm import tqdm
import numpy as np
import cv2


parser = argparse.ArgumentParser()
parser.add_argument("folder_base_dataset", help="enter the path to the folder with tokens") 
args = parser.parse_args()

folder_train = "/train/"
folder_test = "/test/"
folder_validation = "/validation/"

PATH_DATASETS_PARENT = "./datasets_out/"
folder_name_current_dataset = "rfp_data_reduced_" + time.strftime("%d.%m.%Y") + "/"

def copyDataIntoDatasetsOut(base_folder, destination_folder):
    if not exists(destination_folder):
        makedirs(destination_folder)

    all_files = [f for f in listdir(base_folder) if isfile(join(base_folder, f)) and ".gui" in f]
    shuffle(all_files)

    count_files = len(all_files)
    reduced = int(count_files * 0.7)

    print("reducing", base_folder, "from", count_files, "to", reduced)

    reduced_list = all_files[:reduced]

    for file_name_gui in tqdm(reduced_list, desc="copying" + base_folder + " to " + destination_folder):
        copy(base_folder + file_name_gui, destination_folder)

        if "train" in base_folder:
            file_name_npz = file_name_gui.replace(".gui", ".npz")
            copy(base_folder + file_name_npz, destination_folder)
        else:
            file_name_img = file_name_gui.replace(".gui", ".jpg")
            copy(base_folder + file_name_img, destination_folder)

copyDataIntoDatasetsOut( args.folder_base_dataset + folder_train, PATH_DATASETS_PARENT + folder_name_current_dataset + folder_train) 
copyDataIntoDatasetsOut( args.folder_base_dataset + folder_test, PATH_DATASETS_PARENT + folder_name_current_dataset + folder_test) 
copyDataIntoDatasetsOut( args.folder_base_dataset + folder_validation, PATH_DATASETS_PARENT + folder_name_current_dataset + folder_validation) 



            

