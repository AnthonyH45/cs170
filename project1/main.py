#!/usr/bin/python
'''
 This is the main driver code for project 1
 This is where the user gives input
 This is then passed to generic.py 
 and we get back our solution (if there is one)
'''
import random
# from generic import *
from newgeneric import *

def main():
    print("Welcome to Anthony Hallak's 8-puzzle solver!\n")
    try:
        puzzle_type = int(input("Type \"1\" to use a default random puzzle or \"2\" to enter your own\n"))
    except:
        print("Sorry, we could not understand that :(")
        return 1

    if puzzle_type == 1:
        random_arr = [[1,2,3], [4,5,6],[7,8,0]]
        random.shuffle(random_arr[0])
        random.shuffle(random_arr[1])
        random.shuffle(random_arr[2])
        random.shuffle(random_arr)
        print(random_arr[0])
        print(random_arr[1])
        print(random_arr[2])
        problem = random_arr
    elif puzzle_type == 2:
        print("Enter your puzzle, use a zero to represent the blank")
        row_1 = str(input("Enter the first row, use spaces or tabs between numbers\n"))
        row_1 = row_1.split()
        if len(row_1) < 3 or len(row_1) > 3:
            print("That doesn't look like 3 numbers, please try again later")
            return 1
        row_2 = str(input("Enter the second row, use spaces or tabs between numbers\n"))
        row_2 = row_2.split()
        if len(row_2) < 3 or len(row_2) > 3:
            print("That doesn't look like 3 numbers, please try again later")
            return 1
        row_3 = str(input("Enter the third row, use spaces or tabs between numbers\n"))
        row_3 = row_3.split()
        if len(row_3) < 3 or len(row_3) > 3:
            print("That doesn't look like 3 numbers, please try again later")
            return 1

        # convert the str to int
        row_1[0] = int(row_1[0])
        row_1[1] = int(row_1[1])
        row_1[2] = int(row_1[2])
        
        row_2[0] = int(row_2[0])
        row_2[1] = int(row_2[1])
        row_2[2] = int(row_2[2])

        row_3[0] = int(row_3[0])
        row_3[1] = int(row_3[1])
        row_3[2] = int(row_3[2])
        problem = []
        problem.append(row_1)
        problem.append(row_2)
        problem.append(row_3)
    else:
        print("That was not understood, sorry")
    
    
    print("\nEnter your choice of algorithm:")
    print("\t1. Uniform Cost Search")
    print("\t2. A* with the Misplaced Tile Heuristic")
    print("\t3. A* with the Manhattan Distance Heuristic")
    try:
        algo_choice = int(input(""))
    except:
        print("That doesnt look like a number :(")
        return 1

    if algo_choice < 1 or algo_choice > 3:
        print("That was not a valid algorithm choice")
        return 1

    print(problem[0])
    print(problem[1])
    print(problem[2])

    print("Solution?",generic(Problem(problem,8,0,algo_choice)))
    print("Original state",problem)

main()