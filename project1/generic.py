import os
import collections
# this implements the generic search algorithm and takes in a queueing 
# function and an inital problem state for the 8 puzzle

class Problem:
    def __init__(self, arr=[], type=8, goal_state=[]):
        # initial state is the given state from the user
        self.initial_state = arr
        # self.operators = ['left','down','right','up']
        # we turned the above line into tuples to add to traverse the grid
        self.operators = [(-1,0),(0,-1),(1,0),(0,1)]
        if type == 8:
            self.goal_state = [[1,2,3],[4,5,6],[7,8,0]]
        else:
            self.goal_state = goal_state

# Node is a single 3x3 grid representing a state of the 8puzzle 
class Node:
    def __init__(self, state):
        self.state = state

# Turns a problem into a node
def make_node(given_state: Problem):
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
        # and return the list of expansions, not the dictionary

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
        to_ret = []
        for i,j in enumerate(sorted_misplaced):
            print("adding",misplaced[j],"to our return")
            if len(misplaced[j]) > 1: # this means more than one expansion had the same key/score
                for i in misplaced[j]:
                    print("more than one expansion detected for the same score, adding\n",i,"to our return")
                    to_ret.append(i)
            else:
                to_ret.append(misplaced[j][0])
            print()
        print("returning",to_ret)
        return to_ret
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
                print("Expanding")
                print(to_add_arr[0]) #, curr_node[0])
                print(to_add_arr[1]) #, curr_node[1])
                print(to_add_arr[2]) #, curr_node[2])
                print()
                if to_add_arr in seen:
                    print("seen this expansion before, not adding it\n")
                else:
                    to_ret.append(to_add_arr)
                    seen.append(to_add_arr)
    print("returning expansions", to_ret)
    print()
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
        # if len(curr_node[0]) > 1:
        #     curr_node = nodes[0][0]
        #     nodes[0] = nodes[0][1:]
        # else:
            # remove the first node
        nodes = nodes[1:]
        # to_visit = to_visit[1:]
        tick += 1
        print("looking at",curr_node)
        if curr_node == problem.goal_state:
            print("Found goal state!\n")
            return curr_node
        # the node is not the goal state
        # so we expand our nodes and restart
        if tick == 500000:
            print("Tick count of",tick,"Exceeded")
            return "took too long"
        nodes = queueing_function(nodes, expand(curr_node, problem.operators), algo_choice, problem.goal_state)
    return "No solution"

        # if curr_node in seen:
        #     # print("already seen this node, skipping it")
        #     if len(nodes) == 0:
        #         print("Oh no, there isnt another node, looks like no solution :(")
        #         return "No solution"
        #     else:
        #         # while we HAVE seen this node, skip and find the first next unseen
        #         while curr_node in seen:
        #             print("seen this node, skipping", curr_node)
        #             if len(nodes) == 0:
        #                 return "Could not find an unseen node, possible no solution :("
        #             curr_node = nodes[0]
        #             nodes = nodes[1:]
        # else:
        #     seen.append(curr_node)
        # if problem.goal_state(node.state):