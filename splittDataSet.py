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
parser.add_argument("folder_path_gui", help="enter the path to the folder with tokens") 
parser.add_argument("folder_path_img", help="enter the path to the folder with img") 
args = parser.parse_args()

PATH_DATASETS_PARENT = "./datasets_out"
RATIOS_TO_SPLIT = { "train": 0.7, "test": 0.2, "validation": 0.1}
FILE_TYPE = ".jpg"
IMAGE_SIZE = 256

path_gui =  args.folder_path_gui
path_img =  args.folder_path_img

def get_preprocessed_img(img_path, image_size):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (image_size, image_size))
    img = img.astype('float32')
    img /= 255
    return img

def copyDataIntoDatasetsOut(file_list, destination_folder):
    destination = PATH_DATASETS_PARENT + "/" + folder_name_current_dataset + "/" + destination_folder
    if not exists(destination):
        makedirs(destination)

    for file in tqdm(file_list, desc="copy files to " + destination_folder):
        copy(path_gui + file, destination)
        file_name_img = file.replace(".gui", ".jpg")    
        
        if destination_folder != folder_train:
            copy(path_img + file_name_img, destination)
        else:
            file_name_pure = file.replace(".gui", "")    

            img = get_preprocessed_img(path_img + file_name_img, IMAGE_SIZE)

            np.savez_compressed("{}/{}".format(destination, file_name_pure), features=img)
            retrieve = np.load("{}/{}.npz".format(destination, file_name_pure))["features"]

            assert np.array_equal(img, retrieve)




all_gui_files = [f for f in listdir(path_gui) if isfile(join(path_gui, f)) and f != ".gitignore"]

shuffle(all_gui_files)

count_train_images = floor(len(all_gui_files) * RATIOS_TO_SPLIT["train"])
count_test_images = floor(len(all_gui_files) * RATIOS_TO_SPLIT["test"])
count_validation_images = floor(len(all_gui_files) * RATIOS_TO_SPLIT["validation"])

train_list =        all_gui_files[0:count_train_images]
test_list =         all_gui_files[count_train_images:count_train_images+count_test_images]
validation_list =   all_gui_files[count_train_images+count_test_images:]

print("found", len(all_gui_files), "images for training")
print("splitting into: train", len(train_list), "test", len(test_list), "validation", len(validation_list))

folder_name_current_dataset = "rfp_data_" + str(len(all_gui_files)) + "_" + time.strftime("%d.%m.%Y")

folder_train = "/train"
folder_test = "/test"
folder_validation = "/validation"

copyDataIntoDatasetsOut(train_list, folder_train)
copyDataIntoDatasetsOut(test_list, folder_test)
copyDataIntoDatasetsOut(validation_list, folder_validation)