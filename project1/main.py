#!/usr/bin/python
'''
 This is the main driver code for project 1
 This is where the user gives input
 This is then passed to generic.py 
 and we get back our solution (if there is one)
'''
import random
from generic import *

def main():
    print("Welcome to Anthony Hallak's 8-puzzle solver!\n")
    try:
        puzzle_type = int(input("Type \"1\" to use a default random puzzle or \"2\" to enter your own\n"))
    except:
        print("Sorry, we could not understand that :(")
        return 1

    if puzzle_type == 1:
        random_arr = [['1','2','3'], ['4','5','6'],['7','8','0']]
        random.shuffle(random_arr[0])
        random.shuffle(random_arr[1])
        random.shuffle(random_arr[2])
        random.shuffle(random_arr)
        print(random_arr)
        problem = random_arr
    elif puzzle_type == 2:
        print("Enter your puzzle, use a zero to represent the blank")
        row_1 = str(input("Enter the first row, use spaces or tabs between numbers\n"))
        row_1 = row_1.split()
        if len(row_1) < 3 or len(row_1) > 3:
            print("That doesn't look like 3 numbers, please try again later")
            return 1
        row_2 = str(input("Enter the first row, use spaces or tabs between numbers\n"))
        row_2 = row_2.split()
        if len(row_2) < 3 or len(row_2) > 3:
            print("That doesn't look like 3 numbers, please try again later")
            return 1
        row_3 = str(input("Enter the first row, use spaces or tabs between numbers\n"))
        row_3 = row_3.split()
        if len(row_3) < 3 or len(row_3) > 3:
            print("That doesn't look like 3 numbers, please try again later")
            return 1
        problem = [[row_1], [row_2], [row_3]]
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

    if algo_choice > 3 or algo_choice < 1:
        print("That doesn't look like a valid option, sorry")
        return 1

    print(problem)
    generic(Problem(problem), algo_choice)

main()