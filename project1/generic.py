# this implements the generic search algorithm and takes in a queueing 
# function and an inital problem state for the 8 puzzle

class Problem:
    def __init__(self, arr: List[List[int]], type=8, goal_state: List[List[int]]):
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
    def __init__(self, state: List[List[int]]):
        self.state = state

# Turns a problem into a node
def make_node(given_state: Problem):
    return Node(given_state)

# returns a List[Node] to visit
def make_queue(node: Node):
    return [node];

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
def queueing_function(nodes: List[List[int]], expansions: List[List[List[int]]], algo_choice: int, goal_state: List[List[int]]):
    # Says which branch to take
    if algo_choice == 1:
        print("TODO")
    elif algo_choice == 2:
        # for each misplaced tile, we add 1, the lower the better
        # misplaced is an array of misplaced tile nums
        # we add and append as needed
        misplaced_sum = 0
        misplaced = []
        for i in range(0,len(expansions)):
            # we know len(nodes) == 3
            for r in range(0,3):
                # we know len(nodes[0]) == 3
                for c in range(0,3):
                    if expansions[i][r][c] != goal_state[r][c]:
                        misplaced_sum = misplaced_sum + 1
            misplaced.append(misplaced_sum)
        # after we compute all misplaced sums, we want to use the minimal sum
        min_temp = min(misplaced)
        min_arr = [i for i,j in enumerate(misplaced) if j == min_temp]
        # min arr should only contain one value, if it contains more than
        # one value, that means there is more than one good choice, so we 
        # expand that solution 

    elif algo_choice == 3:
        print("TODO")
    else:
        print("TODO")

def find_blank(curr_node: List[List[int]]) -> (int,int):
    for i in range(0,3):
        for j in range(0,3):
            if curr_node[i][j] == 0:
                return (i,j)

'''
1 2 3           1 2 3     1 2 3     1 2 3
4 5 6 => return 4 5 6 and 4 5 6 and 4 0 6
7 0 8           0 7 8     7 8 0     7 5 8
which one to pick depends on the queueing function
this function just expands all possibilities
'''
def expand(curr_node, operators):
    # applies operators to current state to show all possible paths
    # we swap 0 with its surrounding tiles using operators
    to_ret = []
    # find location of 0 = blank and swap it with surrounding ints
    pos_0 = find_blank(curr_node):
    print("Performing operators on", curr_node)
    for i in operators:
        if pos_0[0]+i[0] > -1 and pos_0[0]+i[0] < 3:
            if pos_0[1]+i[1] > -1 and pos_0[1]+i[1] < 3:
                # python allows for negative index, we dont want that
                # pos_swap = ([pos_0[0]+i[0]],[pos_0[1]+i[1]])
                to_add_arr = curr_node
                # swap 0 with current operator position
                temp = to_add_arr[pos_0[0]+i[0]][pos_0[1]+i[1]]
                to_add_arr[pos_0[0]+i[0]][pos_0[1]+i[1]] = 0
                to_add_arr[pos_0[0]][pos_0[1]] = temp
                print("Expanding",to_add_arr)
                to_ret.append(to_add_arr)
    return to_ret

def generic(problem: Problem, algo_choice):
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
        nodes = queueing_function(nodes, expand(curr_node, problem.operators), algo_choice)
    return "No solution"