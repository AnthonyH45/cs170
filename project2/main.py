from io import TextIOWrapper
from typing import *

def validate(data, j):
    return j[0]

def fs(data: List[List[float]]):
    for i,j in enumerate(data):
        print("On level:",i)
        to_add_level = [] # make set so we dont add
        best_accuracy = 0
        for i in range(1,len(j)):
            print("--Considering adding the",i,"feature")
            current_accuracy = validate(data,j[1:])
            print("val:",j)
            if best_accuracy < current_accuracy:
                best_accuracy = current_accuracy
                to_add_level.append(j)
        print("Best feature to add on level",i,"is feature",to_add_level[-1])

# https://stackoverflow.com/questions/6492096/automatically-process-numbers-in-e-scientific-notation-in-python
# https://stackoverflow.com/questions/44461551/how-to-print-map-object-with-python-3
# https://docs.python.org/3/library/functions.html
# https://www.geeksforgeeks.org/read-a-file-line-by-line-in-python/
# https://docs.python.org/3/library/io.html#io.TextIOBase
# CS170_largetestdata__9.txt
# CS170_SMALLtestdata__72.txt

# reads the given TextIOWrapper 
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

main()