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
            self.goal_state = [['1','2','3'],['4','5','6'],['7','8','0']]
        else:
            self.goal_state = goal_state

class Node:
    def __init__(self, state):
        self.state = state

def make_node(given_state):
    # TODO
    return 0

def make_queue(node_arr):
    # TODO
    return 0

# option
# 1 = Uniform Cost (A* with h(n) == 0)
# 2 = A* with Misplaced Tile h(n)
# 3 = A* with Manhattan Distance h(n)
def queueing_function(option, nodes, expansions):
    # TODO
    return 0

def expand(curr_node, operators):
    # TODO 
    return 0

def generic(problem: Problem, option_choice):
    # we need to make a list of nodes that have an order to visit
    nodes = make_queue(make_node(problem.initial_state))
    while True:
        if len(nodes) == 0:
            return "No solution"
        # pop off the first node of the queue
        curr_node = nodes[0]
        # remove the first node
        nodes = nodes[1:]
        # if problem.goal_state(node.state):
        if curr_node in problem.goal_state:
            return curr_node
        # the node is not the goal state
        # so we expand our nodes and restart
        nodes = queueing_function(option_choice, nodes, expand(curr_node, problem.operators))
    return "No solution"
