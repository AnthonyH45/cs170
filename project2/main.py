from io import TextIOWrapper
import math
import time
from typing import *

# https://stackoverflow.com/questions/4362586/sum-a-list-of-numbers-in-python
# takes in data, j (current row), (r,c) location of j in data
def validate(data: List[List[float]], curr: List[float], r: int): #, c: int):
    num_correct = 0
    nns = []
    for i,j in enumerate(data):
        # print("finding nn for",j)
        nn_dist = float('INF')
        nn_loc = float('INF')
        nn_class = float(0)
        if i != r:
            dist = math.sqrt(sum([(a-b)**2 for (a,b) in zip(j[1:],curr)]))
            if dist < nn_dist:
                nn_dist = dist
                nn_loc = i
                nn_class = j[0]
                nns.append(j)

    time.sleep(1)
    print(nns)
    time.sleep(1)
    for n in nns:
        if n[0] == curr[0]:
            num_correct += 1

    acc = (num_correct / len(data))
    print("Accuracy:",acc)
    return acc
    

def fs(data: List[List[float]]):
    # set of tuples (category, feature)
    to_add_level = set() 
    for i,j in enumerate(data):
        print("On level:",i)
        best_accuracy = 0
        for k in range(1,len(j)):
            if (i,k) not in to_add_level:
                print("--Considering adding the",k,"feature")
                current_accuracy = validate(data,j[1:], i) #, k)
                time.sleep(1)
                print("val:",j)
                if best_accuracy < current_accuracy:
                    best_accuracy = current_accuracy
                    to_add_level.add((i,k))

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
        # parsed_data is 500 rows by 101 columns (100 features excluding 1st column for label)
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