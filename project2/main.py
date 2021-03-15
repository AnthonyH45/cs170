from io import TextIOWrapper
import math
import time
from typing import *

# https://stackoverflow.com/questions/4362586/sum-a-list-of-numbers-in-python
# takes in data, curr_features, feat_to_add is the column of the feature to add
def validate(data: List[List[float]], curr_feature: set(), curr_class, feat_to_add) -> float:
    num_correct = 0
    instances = [i[0] for i in data].count(curr_class)

    for i,j in enumerate(data):
        # print("finding nn for",j)
        # time.sleep(1)
        # obj_to_class = j[1:]
        # obj_to_class_class = j[0]

        nn_dist = float('INF')
        nn_loc = float('INF')
        nn_class = 0
        for k,l in enumerate(data):
            if i != k:
                # print("Asking if",l)
                # only use the features in curr_feature and feat_to_add
                to = [n for m,n in enumerate(j) if m in curr_feature or m == feat_to_add]
                # print(to)
                nn = [n for m,n in enumerate(l) if m in curr_feature or m == feat_to_add]
                # print(nn)
                dist = math.sqrt(sum([(a-b)**2 for (a,b) in zip(to,nn)]))
                # print(dist)
                if dist < nn_dist:
                    nn_dist = dist
                    nn_loc = k
                    nn_class = l[0]
                # time.sleep(15)

        if nn_class == j[0]:
            num_correct = num_correct + 1

    acc = num_correct / instances
    print("num correct / num instances = acc |",num_correct,"/",instances,"=",acc)
    # time.sleep(10)
    return acc

def fs(data: List[List[float]]):
    # start empty and add highest accuracy feature at each level
    curr_features = set() 
    for i,j in enumerate(data):
        print("On level:",i+1)
        # time.sleep(0.5)
        best_accuracy: float = 0
        best_feat: int = 0

        # out of C features, find the highest accuracy
        j_class = j[0]
        for k in range(1,len(j)): # start at 1 to ignore first column (label/class)
            # if we have not seen this feature
            if k not in curr_features:
                print("--Considering adding the",k,"feature")
                # time.sleep(0.5)
                # check the accuracy of the kth feature with our current feature list
                current_accuracy = validate(data,curr_features,j_class, k)

                if best_accuracy < current_accuracy:
                    best_accuracy = current_accuracy
                    best_feat = k

        curr_features.add(best_feat)
        print("On level",i+1,"we add feature",best_feat)
        print("Current features:",curr_features)
        time.sleep(20)

# https://stackoverflow.com/questions/6492096/automatically-process-numbers-in-e-scientific-notation-in-python
# https://stackoverflow.com/questions/44461551/how-to-print-map-object-with-python-3
# https://docs.python.org/3/library/functions.html
# https://www.geeksforgeeks.org/read-a-file-line-by-line-in-python/
# https://docs.python.org/3/library/io.html#io.TextIOBase
# CS170_largetestdata__9.txt
# CS170_SMALLtestdata__72.txt
# reads the given TextIOWrapper 
# parses the txt file and converts the 
# numbers to proper floats, rather than scientific number
def parse(f: TextIOWrapper):
    return [[float(j) for j in i.split()] for i in f.readlines()]

def main():
    print("Welcome to Anthony Hallak's Feature Selection Algorithm!")

    filename = str(input("Type in the name of the file to test: "))
    try:
        parsed_data = parse(open(filename))
        # parsed_data is R rows by C columns (C-1 features excluding 1st column for label)
    except:
        print("Sorry, could not open that filename, please make sure it exists in this directory, you have sufficient permissions, and  exiting")
        return

    algo_choice = int(input("\nType the number of the algorithm you want to run.\n1) Forward Selection\n2) Backward Elimination\n"))

    if algo_choice < 1 or algo_choice > 2:
        print("Sorry, that is not a valid algorithm choice, exiting")
        return
    
    if algo_choice == 1:
        print("Using Forward Selection")
        fs(parsed_data)
    else:
        print("Using Backward Elimination")
        be(parsed_data)

if __name__ == '__main__':
    main()