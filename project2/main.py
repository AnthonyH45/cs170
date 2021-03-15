from io import TextIOWrapper
import math
import time
from typing import *

# https://stackoverflow.com/questions/4362586/sum-a-list-of-numbers-in-python
# takes in data, j (current row), (r,c) location of j in data
def validate(data: List[List[float]], curr: List[float], r: int, c: int) -> float:
    num_correct: int = 0
    nns: List[List[float]] = []

    for i,j in enumerate(data):
        # print("finding nn for",curr[0],r,c)
        nn_dist = float('INF')
        nn_loc = float('INF')
        nn_class = float(0)

        if i != r:
            dist = math.sqrt(sum([(a-b)**2 for (a,b) in zip(j[1:],curr)]))
            if dist < nn_dist:
                nn_dist = dist
                nn_loc = i
                nn_class = j[0]
                # print("Found nn: (dist loc class):(",nn_dist,nn_loc,nn_class,")")
                nns.append(j)

    for n in nns:
        print(n[0],curr[0],n[0] == curr[0])
        if n[0] == curr[0]:
            num_correct += 1

    acc = (float(num_correct) / len(data))
    print(num_correct,len(data),acc)
    # print("Accuracy:",acc)
    time.sleep(0.5)
    return acc

def fs(data: List[List[float]]):
    # set of tuples (level, feature)
    # start empty and add highest accuracy feature at each level
    add_feature = set() 
    for i,j in enumerate(data):
        # print("On level:",i+1)
        best_accuracy: float = 0
        best_feat: int = 0

        # out of C features, find the highest accuracy
        for k in range(1,len(j)):

            # if we have not seen this feature
            if k not in add_feature:
                # print("--Considering adding the",k,"feature")
                current_accuracy = validate(data,j, i, k)

                if best_accuracy < current_accuracy:
                    best_accuracy = current_accuracy
                    best_feat = k

        add_feature.add(best_feat)
        print("On level",i+1,"we add feature",best_feat)
        time.sleep(1)

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