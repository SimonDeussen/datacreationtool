import argparse

from os import listdir
from os.path import join, isfile
import math
from collections import Counter

from assets.Utils import *

def getRowType(row):
    types = {   
                0: ["single"],
                1: ["double", "double"],
                2: ["double", "quadruple", "quadruple"],
                3: ["quadruple", "double", "quadruple"],
                4: ["quadruple", "quadruple", "double"],
                5: ["quadruple", "quadruple", "quadruple", "quadruple"]
            }
    
    row_children = []
    for child in row.children:
        row_children.append(child.tag_name)
        
    for i in range(6):
        if Counter(types[i]) == Counter(row_children):
            return i
                    
    return False
    
def getTokenListFromFile(filepath):
    with open(filepath) as data_file:
        tokenString = data_file.read()
    
    cleaned = tokenString.replace("},", "}")
    cleaned = cleaned.replace("{", " {")

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

def compareResults(comparison):
    error_object = {
                        "isHeaderCorrect": None, 
                        "differenceMenuButtons" : None,
                        "differenceRowCount": None,
                        "countWrongButtons": None,
                        "countCorrectButtons": None,
                        "differenceButtonCount": None,
                        "differenceTokenCount": None,
                        "trueFileName": None,
                        "trueHeaderType": None,
                        "countWrongRowType": None,
                        "countCorrectRowType": None,
                        "predictedFileName": None,
                        "true_token_count": None
                        }

    truth = comparison["truth"]
    prediction = comparison["prediction"]

    truth_tokens = getTokenListFromFile(path_truths + truth)
    predictions_tokens = getTokenListFromFile(path_predictions + prediction)

    root_truth = Utils.createElementsFromTokenList(truth_tokens.copy())
    root_prediction = Utils.createElementsFromTokenList(predictions_tokens.copy())

    error_object["trueFileName"] = path_truths + truth
    error_object["predictedFileName"] = path_predictions + prediction

    error_object["trueHeaderType"] = root_truth.children[0].tag_name
    error_object["isHeaderCorrect"] = "sidebar" in truth_tokens and "sidebar" in predictions_tokens or "header" in truth_tokens and "header" in predictions_tokens
    error_object["differenceTokenCount"] = int( len(predictions_tokens) - len(truth_tokens))
    error_object["true_token_count"] = len(truth_tokens)

    # COUNT MENUE BUTTONS
    if root_truth.children[0].tag_name in ["sidebar", "header"]:
        true_count_menu_buttons = len(root_truth.children[0].children)

    if root_prediction.children[0].tag_name in ["sidebar", "header"]:
        pred_count_menu_buttons = len(root_prediction.children[0].children)    

    error_object["differenceMenuButtons"] = int(pred_count_menu_buttons-true_count_menu_buttons)

    # COUNT ROWS
    true_rows = []
    for child in root_truth.children:
        if child.tag_name == "row":
            true_rows.append(child)

    pred_rows = []
    for child in root_prediction.children:
        if child.tag_name == "row":
            pred_rows.append(child)

    error_object["differenceRowCount"] = int(len(pred_rows) - len(true_rows))

    # CHECK ROW TYPES
    count_wrong_rows = 0
    count_correct_rows = 0
    for i in range(len(pred_rows)):
        if getRowType(pred_rows[i]) == getRowType(true_rows[i]):
            count_correct_rows += 1
        else:
            count_wrong_rows += 1


    error_object["countWrongRowType"] = count_wrong_rows
    error_object["countCorrectRowType"] = count_correct_rows

    # CHECK CORRECT BUTTONS
    true_buttons = []
    for row in true_rows:
        for row_element in row.children:
            for child in row_element.children:
                if "btn" in child.tag_name:
                    true_buttons.append(child.tag_name)

    pred_buttons = []
    for row in pred_rows:
        for row_element in row.children:
            for child in row_element.children:
                if "btn" in child.tag_name:
                    pred_buttons.append(child.tag_name)

    difference_button_count = int(len(pred_buttons) - len(true_buttons))

    correct_buttons = 0
    wrong_buttons = 0
    for i in range(len(pred_buttons)):
        try:
            if pred_buttons[i] == true_buttons[i]:
                correct_buttons += 1
            else:
                wrong_buttons += 1
        except Exception as ex:
            pass

    error_object["countWrongButtons"] = wrong_buttons
    error_object["countCorrectButtons"] = correct_buttons
    error_object["differenceButtonCount"] = difference_button_count
    
    return error_object


# parser = argparse.ArgumentParser()
# parser.add_argument("folder_path_gui_truth", help="enter the path to the folder with truth") 
# parser.add_argument("folder_path_gui_predicted", help="enter the path to the folder all predictions") 
# args = parser.parse_args()

# path_predictions = args.folder_path_gui_predicted
# path_truths = args.folder_path_gui_truth

# all_predictions = [f for f in listdir(path_predictions) if isfile(join(path_predictions, f))]
# all_truths =      [f for f in listdir(path_truths) if isfile(join(path_truths, f))]


# print("Found", len(all_predictions), "predictions at", path_predictions)
# print("Found", len(all_truths), "truths at", path_truths)

# predictions_with_truth = []
# for prediction in all_predictions:
#     for truth in all_truths:
#         if prediction == truth:
#             predictions_with_truth.append({"prediction": prediction, "truth": truth})

# print("Found", len(predictions_with_truth), "predictions with truths")
# print("Scoring now...")

predictions_with_truth = [{"truth": "./generatedMarkup/SECOND_complete_generation_4_04.10.2018_1538655331945.gui",
                           "prediction": "./generatedMarkup/second.gui"}]
path_truths = ""
path_predictions = ""

results = []
for comparison in predictions_with_truth:
    errors = compareResults(comparison)
    results.append(errors)

print(results)