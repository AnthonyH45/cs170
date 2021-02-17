from typing import *
# fixes 'type object is not subscritptable' error
# taken from https://stackoverflow.com/questions/24853923/type-hinting-a-collection-of-a-specified-type
import time

'''
Node:
    - state: 3x3 grid representing a state in the 8 puzzle
    - depth: holds the depth from the given problem
    - score: based on user selected heuristic
    - find_blank(): returns (i,j) position of 0 in state
    - print(): prints each row of the state and a newline at the end
'''
class Node:
    def __init__(self, state: List[List[int]]=[[1,2,3],[4,5,6],[7,8,0]], depth: int = 0, score: int = 0):
        self.state = state  # 3x3 grid
        self.depth = depth  # g(n)
        self.score = score  # f(n) = g(n) + h(n)
        self.operators = [(-1,0),(0,-1),(1,0),(0,1)] # (x,y) : left, down, right, up

    def find_blank(self):
        for i in range(0,len(self.state)):
            for j in range(0,len(self.state[0])):
                if self.state[i][j] == 0:
                    return (i,j)

    def print(self):
        print(self.state[0],'\tDepth, g(n):',self.depth)
        print(self.state[1],'\tScore, h(n):',self.score-self.depth)
        print(self.state[2],'\tf(n)',self.score)
        print()

    # https://docs.python.org/3/reference/datamodel.html#object.__eq__
    # https://stackoverflow.com/questions/4169252/remove-duplicates-in-list-of-object-with-python/4173307
    def __eq__(self, other):
        return self.state == other.state

    # https://docs.python.org/3/reference/datamodel.html#object.__hash__
    # https://stackoverflow.com/questions/626759/whats-the-difference-between-lists-and-tuples
    # https://stackoverflow.com/questions/11142397/does-python-have-an-immutable-list
    # https://stackoverflow.com/questions/19371358/python-typeerror-unhashable-type-list/19371472
    # we need an immutable type for hashing in a set
    # so we return a serialized state as a tuple
    def __hash__(self):
        return hash( 
                    (self.state[0][0],self.state[0][1],self.state[0][2],
                     self.state[1][0],self.state[1][1],self.state[1][2],
                     self.state[2][0],self.state[2][1],self.state[2][2])
                    )

'''
Problem:
    - arr: 3x3 grid to make a initial Node state
    - puzzle_type: specifies the type of puzzle to solve
    - goal_state: 3x3 grid to find a path to
    - algo_choice: determines which heuristic to use
    - make_node(): returns self.init_state node
    - make_queue(node): returns [node]
    - expand(node, operators): returns a list of expanded nodes, the blank is swapped using the operators
    - queueing_function(node, expansions): gives each expansion a score according to the heuristic, and appends each node to it
'''
class Problem:
    def __init__(self, arr: List[List[int]] = [[1,2,3],[4,5,6],[7,8,0]], puzzle_type: int = 8, goal_state: List[List[int]] = [[1,2,3],[4,5,6],[7,8,0]], algo_choice: int = 2):
        self.init_state = Node(arr,0,0)     # inital state is a node with 0 depth and 0 score
        self.puzzle_type = puzzle_type      # determines which puzzle to sovle, right now, only 8 puzzle
        self.seen_set = set()               # use set instead to have O(1) checks for duplicates
        self.exp_set = set()
        self.algo_choice = algo_choice      # determines which heuristic to use
        self.num_exp = 0                    # keeps track of the number of expansions
        if self.puzzle_type == 8:
            self.goal_state = Node([[1,2,3],[4,5,6],[7,8,0]],0,0)
        else:
            self.goal_state = Node(goal_state,0,0)

    def make_node(self):
        return self.init_state

    def make_queue(self, node: Node):
        return [node]

    def expand(self, node: Node, operators):
        print("Expanding")
        to_ret = []
        pos_0 = node.find_blank()
        self.exp_set.add(node)
        for i in operators:
            if (pos_0[0]+i[0]) > -1 and (pos_0[0]+i[0]) < 3:
                if (pos_0[1]+i[1]) > -1 and (pos_0[1]+i[1]) < 3:
                    to_add_node = Node([[j for j in l] for l in node.state],node.depth+1, node.depth+1)
                    temp = to_add_node.state[pos_0[0]+i[0]][pos_0[1]+i[1]]
                    to_add_node.state[pos_0[0]+i[0]][pos_0[1]+i[1]] = 0
                    to_add_node.state[pos_0[0]][pos_0[1]] = temp

                    # deal with duplicates in queueing ?
                    # we have less nodes expanded but takes longer
                    if to_add_node in self.exp_set:
                        print("already seen this expansion, not adding it to queue")
                    else:
                        # to_add_node.print()
                        to_ret.append(to_add_node)
                        self.exp_set.add(to_add_node)
                    # to_ret.append(to_add_node)

        if len(to_ret) == 0:
            return []

        self.num_exp += len(to_ret)

        return to_ret

    def queueing_function(self, nodes: List[Node], expansions: List[Node]):
        if self.algo_choice == 1:
            print("Using Uniform Cost Search")
            # since everything costs the same, we just add the 
            # expansions to the nodes and return
            for i in expansions:
                if i not in self.seen_set:
                    nodes.append(i)
                    self.seen_set.add(i)
                
            print("Best node with g(n)=", nodes[0].depth, "and h(n)=",nodes[0].score - nodes[0].depth)
            nodes[0].print()
            return nodes

        if self.algo_choice == 2:
            print("Using A* with misplaced tile heuristic")

            to_ret = []
            for exp in expansions:
                if exp not in self.seen_set: # if we have not seen this node, lets look at it
                    if exp.state == self.goal_state.state:
                        print("Found goal state in queueing, returning!")
                        return [exp]

                    misplaced_sum = 0
                    for i in range(0,len(exp.state)): # we know 8 puzzle is 3x3
                        for j in range(0,len(exp.state[0])): # so no need to call len(exp.state) and len(exp.state[0])
                            # for each misplaced tile, we add one to the score
                            if exp.state[i][j] != 0:
                                if exp.state[i][j] != self.goal_state.state[i][j]:
                                    misplaced_sum = misplaced_sum + 1
                    # score is already assigned to depth
                    # score = f(n) = g(n) + h(n)
                    # g(n) is the _cost to_ aka the depth, already assigned in the expansion
                    # h(n) is the heuristic score, aka the manhattan or misplaced
                    # so we just add h(n) to g(n) and be done!
                    exp.score += misplaced_sum
                    to_ret.append(exp)
                    self.seen_set.add(exp)

            # sort expansions by misplaced tiles, smallest first
            # used this https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
            to_ret.sort(key=lambda x: x.score)
            for i in to_ret:
                nodes.append(i)
            print("Best node with g(n)=", nodes[0].depth, "and h(n)=",nodes[0].score - nodes[0].depth)
            nodes[0].print()
            
            return nodes

        if self.algo_choice == 3:
            print("Using A* with manhattan distance heuristic")

            to_ret = []
            third = [2,0,1]
            for exp in expansions:
                if exp.state == self.goal_state.state:
                    print("Found goal state in queueing, returning!")
                    return [exp]

                # if exp.state in self.seen:
                    # a = 1
                # else:
                # if True:
                if exp not in self.seen_set:
                    manhattan_d = 0
                    # for each square in the state, we find how far from its goal state square it is
                    # each number's distance is summed and that is assgined as the nodes score  
                    for i in range(0,len(exp.state)):
                        for j in range(0,len(exp.state[0])):
                            # this took a while to figure out, but it maps numbers [0,8] to their respective position in the goal state!
                            # since python treats bools like C/C++, we can use a branchless statement to check for 0 and add 2 in one go!
                            if exp.state[i][j] != 0:
                                # len(exp.state[0]) == 3 for 8 puzzle
                                r = ((exp.state[i][j] - 1)// len(exp.state[0])) #+ ((exp.state[i][j] == 0)*2) ) # gets the row of the i,j in the goal state
                                c = third[ (exp.state[i][j] % len(exp.state[0])) ]                              # gets the column of the i,j in the goal state
                                # take the difference between the goal and current positions, that is the distance, similar to distance formula from math class!
                                manhattan_d += ( abs(r-i) + abs(c-j) )
                    # score is already assigned to depth
                    # score = f(n) = g(n) + h(n)
                    # g(n) is the _cost to_ aka the depth
                    # h(n) is the heuristic score, aka the manhattan or misplaced
                    # so we just add h(n) to g(n) and be done!
                    exp.score += manhattan_d
                    to_ret.append(exp)
                    self.seen_set.add(exp)

            # sort list of nodes by score
            # used this https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
            to_ret.sort(key=lambda x: x.score)
            # nodes.sort(key=lambda x: x.score)
            for i in to_ret:
                nodes.append(i)
            # for i in nodes:
                # to_ret.append(i)
            # nodes.sort(key=lambda x: x.score)
            print("Best node with g(n)=", nodes[0].depth, "and h(n)=",nodes[0].score - nodes[0].depth)
            nodes[0].print()

            return nodes

    def print_algo(self):
        if self.algo_choice == 1:
            print("Used Uniform Cost Search")
        elif self.algo_choice == 2:
            print("Used A* with Misplaced Tiles as the heuristic")
        elif self.algo_choice == 3:
            print("Used A* with Manhattan Distance as the heuristic")
        else:
            print("Used ???")

def generic(problem: Problem, algo_choice=2):
    if problem.init_state.state == problem.goal_state.state:
        return "Hey! The initial state is already solved!"

    nodes = [problem.init_state]
    start = time.time()
    max_num_nodes = -1
    while True:
        if len(nodes) == 0:
            return "No Solution :("

        max_num_nodes = max( [ len(nodes),max_num_nodes ] )
        curr_node = nodes[0]
        nodes = nodes[1:]
        problem.seen_set.add(curr_node)

        # print("Current Depth:",curr_node.depth)
        # print("Looking at")
        # curr_node.print()

        if curr_node.state == problem.goal_state.state:
            end = time.time()
            problem.print_algo()
            print("Found solution at depth", curr_node.depth)
            print("Total number of expanded nodes:", len(problem.exp_set))#problem.num_exp)
            print("Total number of seen nodes:",len(problem.seen_set))
            print("Largest queue size:",max_num_nodes)
            print("Seconds elapsed WITHOUT printing:", end-start)
            return curr_node.state

        # if we have been runnning for 90 minutes and did not find a solution, quit
        if time.time() - start > 5400:
            print("depth of",curr_node.depth,"and no solution, quitting")
            print("Total number of expanded nodes:", problem.num_exp)
            print("Total number of seen nodes:",len(problem.seen))
            return "took too long"

        nodes = problem.queueing_function(nodes, problem.expand(curr_node,curr_node.operators))
    return "No solution"


# this implements the generic search algorithm and takes in a queueing 
# function and an inital problem state for the 8 puzzle
import collections
import os

# Node is a single 3x3 grid representing a state of the 8puzzle
# depth is where it is in the tree
# score is for heuristic 
# -- used for number of misplaced in Misplaced Tile
# -- used for distance for Manhattan Distance
class Node:
    def __init__(self, state, depth, score):
        self.state = state
        self.depth = depth
        self.score = score 

class Problem:
    def __init__(self, arr=[[],[],[]], type=8, goal_state=[[],[],[]]):
        # initial state is the given state from the user
        self.initial_state = self.make_node(arr,0,0) # this is the root node of the tree
        # self.operators = ['left','down','right','up']
        # we turned the above line into tuples to add to traverse the grid
        self.operators = [(-1,0),(0,-1),(1,0),(0,1)]
        if type == 8:
            self.goal_state = [[1,2,3],[4,5,6],[7,8,0]]
        else:
            self.goal_state = goal_state

    def make_node(given_p: Problem):
        return Node(given_state)

    # returns a List[Node] to visit
    # to_visit = []
    def make_queue(node: Node):
        # to_visit.append(node.state)
        return [node.state];
    

'''
nodes is the current state
expansions is a list of states from expand()
algo_choice is the user selected algorithm
goal_state is the goal state
algo_choice = 
    1. Uniform Cost Search
    2. A* with misplaced
    3. A* with manhattan
A*: f(n) = g(n) + h(n)
g(n) is the cost to goto a node
h(n) is the estimated distance to the goal
'''
# to_ret = []
def queueing_function(nodes, expansions, algo_choice, goal_state):
    # Says which branch to take
    if algo_choice == 1:
        # since uniform cost is all the same, the order of expansions
        # can be assumed to be the order to traverse
        for i in expansions:
            nodes.append(i)
        return nodes
    elif algo_choice == 2:
        print("Using misplaced tile heuristic to order the expansions")
        # we have a dictionary that maps scores to their expansions
        # key -> value ; score -> list[expansions[i]]
        # we use a list to append expansions that have the same score
        # we then sort the dictionary by the score
        # and return the ordered list of expansions, not the dictionary

        # for each misplaced tile, we add 1, the lower the better
        # misplaced is the dictionary
        # we add and append as needed
        misplaced = {}
        for i in range(0,len(expansions)):
            if expansions[i] == goal_state:
                # if an expansions is the goal state, no need to do any work, just return
                return [expansions[i]]
            # we know len(nodes) == 3
            misplaced_sum = 0
            for r in range(0,3):
                # we know len(nodes[0]) == 3
                for c in range(0,3):
                    if expansions[i][r][c] != goal_state[r][c]:
                        # print(i,r,c,expansions[i][r][c],"!=",goal_state[r][c])
                        misplaced_sum = misplaced_sum + 1
            print("misplaced score", misplaced_sum,"for",expansions[i])
            if misplaced_sum not in misplaced:
                print("Current expansion has a unique score, adding", [expansions[i]],"\n")
                misplaced[misplaced_sum] = [expansions[i]]
            else:
                # if two expansions have the same score, 
                print("Already a score for this expansion\nappending to existing score",expansions[i],"\n")
                misplaced[misplaced_sum].append(expansions[i])
            print()
            # misplaced[misplaced_sum] = expansions[i]
        # sort by key
        # sorted_misplaced = sorted(misplaced, key=misplaced.get)
        sorted_misplaced = collections.OrderedDict(sorted(misplaced.items()))

        # print("Sorted dictionary:", sorted_misplaced)
        # to_ret = []
        for i,j in enumerate(sorted_misplaced):
            print("adding",misplaced[j],"to our return")
            if len(misplaced[j]) > 1: # this means more than one expansion had the same key/score
                for i in misplaced[j]:
                    print("more than one expansion detected for the same score, adding\n",i,"to our return")
                    nodes.append(i)
            else:
                nodes.append(misplaced[j][0])
            print()
        print("returning",nodes)
        return nodes
    elif algo_choice == 3:
        print("TODO")
        os.exit(1)
    else:
        print("TODO")
        os.exit(1)

def find_blank(curr_node):
    # print("Finding blank in", curr_node)
    for i in range(0,3):
        # print("i:",i)
        for j in range(0,3):
            # print("j:",j)
            # print("Looking at [i][j]",i,j) #,curr_node[i][j])
            if curr_node[i][j] == 0:
                # print("found blank at:",i,j)
                return (i,j)
    # guaranteed to find a blank, so no need to catch it

'''
1 2 3           1 2 3     1 2 3     1 2 3
4 5 6 => return 4 5 6 and 4 5 6 and 4 0 6
7 0 8           0 7 8     7 8 0     7 5 8
which one to pick depends on the queueing function
this function just expands all possibilities
'''

# this seen set is to prevent seen states recursing over and over each other, preventing us from solving the problem
# seen = set() # this breaks bc lists are not hashable
seen = []
def expand(curr_node, operators):
    # applies operators to current state to show all possible paths
    # we swap 0 with its surrounding tiles using operators
    to_ret = []
    # find location of 0 = blank and swap it with surrounding ints
    pos_0 = find_blank(curr_node)
    print("Performing operators on")
    print(curr_node[0])
    print(curr_node[1])
    print(curr_node[2])
    print()
    # to_add_arr = []
    for i in operators:
        # make sure the operators expand within the bounds
        if pos_0[0]+i[0] > -1 and pos_0[0]+i[0] < 3:
            # we dont want to index with negative values as python treats it as index in reverse
            if pos_0[1]+i[1] > -1 and pos_0[1]+i[1] < 3:
                # python allows for negative index, we dont want that
                to_add_arr = [[j for j in i] for i in curr_node]
                # swap 0 with current operator position
                temp = to_add_arr[pos_0[0]+i[0]][pos_0[1]+i[1]]
                to_add_arr[pos_0[0]+i[0]][pos_0[1]+i[1]] = 0
                to_add_arr[pos_0[0]][pos_0[1]] = temp
                print("Expanding to")
                print(to_add_arr[0]) #, curr_node[0])
                print(to_add_arr[1]) #, curr_node[1])
                print(to_add_arr[2]) #, curr_node[2])
                print()
                if to_add_arr in seen:
                    print("seen this expansion before, not adding it\n")
                else:
                    to_ret.append(to_add_arr)
                    seen.append(to_add_arr)
    print("returning expansions", to_ret, "\n")
    return to_ret

def generic(problem: Problem, algo_choice=2):
    if problem.initial_state == problem.goal_state:
        return "Hey! The initial state is already solved!"
    # we need to make a list of nodes that have an order to visit
    nodes = make_queue(make_node(problem.initial_state))
    tick = 0
    while True:
        if len(nodes) == 0:
            return "No solution"
        # pop off the first node off the queue
        curr_node = nodes[0]
        nodes = nodes[1:]
        tick += 1
        print("looking at",curr_node)
        if curr_node == problem.goal_state:
            print("Found goal state! Total expansions", tick, "\n")
            return curr_node
        # tick count represents maximum expansions
        if tick == 500000:
            print("Tick count of",tick,"Exceeded")
            return "took too long"
        # the node is not the goal state   
        # so we expand our nodes and restart
        nodes = queueing_function(nodes, expand(curr_node, problem.operators), algo_choice, problem.goal_state)
    return "No solution"
    
    '''
NOTE
Please run this python script like the following
`python3 tester.py 1>trace_upto20_desktop.txt`
in order to save the traces
with silver search installed, run
`ag "at depth" -B 1 -A 6 trace_upto20_desktop.txt`
to print out 1 line before and 6 lines after the match of "at depth"
In one command:
python3 tester.py 1>trace_upto20_desktop.txt && ag "at depth" -B 1 -A 6 trace_upto20_desktop.txt

NOTE 2:
1 == uniform
2 == misplaced
3 == manhattan

this is going to go through the problems given from the prof
run them with each algo and the redirection will put it in a file for us
we can then look at the results later
'''
# =================================================
from newgeneric import *
import time
# list of tuples with ( depth, problem )
# all problems were given from prof
problems = [
    (0, [[1,2,3],[4,5,6],[7,8,0]]), # depth 0
    (2, [[1,2,3],[4,5,6],[0,7,8]]), # depth 2
    (4, [[1,2,3],[5,0,6],[4,7,8]]), # depth 4
    (8, [[1,3,6],[5,0,2],[4,7,8]]), # depth 8
    (12, [[1,3,6],[5,0,7],[4,8,2]]), # depth 12
    (16, [[1,6,7],[5,0,3],[4,8,2]]), # depth 16
    (20, [[7,1,2],[4,8,5],[6,3,0]]), # depth 20
    (24, [[0,7,2],[4,6,1],[3,5,8]]), # depth 24
    (31, [[8,6,7],[2,5,4],[3,0,1]]), # depth 31
    (31, [[6,4,7],[8,5,0],[3,2,1]]), # depth 31
]
algo_choice = [1,2,3]

for p in problems:
    print("=================================================")
    for a in algo_choice:
        print("START")
        print("Solution?",generic(Problem(p[1],8,0,a)))
        print("Original state",p[1])
        print("END")
        print()
        time.sleep(1)
    print("=================================================")


#!/usr/bin/python3
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
        puzzle_type = int(input("Type \"1\" to use a default puzzle or \"2\" to enter your own or \"3\" for a random puzzle!\n"))
    except:
        print("Sorry, we could not understand that :(")
        return 1

    if puzzle_type == 3:
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
        row_1 = str(input("Enter the first row, use spaces or tabs between numbers    "))
        row_1 = row_1.split()
        if len(row_1) < 3 or len(row_1) > 3:
            print("That doesn't look like 3 numbers, please try again later")
            return 1
        row_2 = str(input("Enter the second row, use spaces or tabs between numbers   "))
        row_2 = row_2.split()
        if len(row_2) < 3 or len(row_2) > 3:
            print("That doesn't look like 3 numbers, please try again later")
            return 1
        row_3 = str(input("Enter the third row, use spaces or tabs between numbers    "))
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
    elif puzzle_type == 1:
        # arr = [[4,1,3],[7,0,6],[8,5,2]] 
        # arr = [[7,1,2],[4,8,5],[6,3,0]] # depth 20 ; given from prof
        arr = [[1,6,7],[5,0,3],[4,8,2]] # depth 16 ; given from prof
        print(arr[0])
        print(arr[1])
        print(arr[2])
        problem = arr
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