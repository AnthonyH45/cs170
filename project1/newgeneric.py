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
        self.algo_choice = algo_choice      # determines which heuristic to use
        self.num_exp = 0                    # keeps track of the number of expansions
        if self.puzzle_type == 8:
            self.goal_state = Node([[1,2,3],[4,5,6],[7,8,0]],0,0)
        else:
            self.goal_state = Node(goal_state,0,0)

    # init_state is already a node, return it
    def make_node(self):
        return self.init_state

    # this is equivalent to [problem.init_state]
    # put here to match general search algorithm given from prof
    def make_queue(self, node: Node):
        return [node]

    def expand(self, node: Node, operators):
        print("Expanding")
        to_ret = []
        pos_0 = node.find_blank()
        # add the passed in node to our seen_set, so we do not visit again later
        self.seen_set.add(node)
        for i in operators:
            if (pos_0[0]+i[0]) > -1 and (pos_0[0]+i[0]) < 3:
                if (pos_0[1]+i[1]) > -1 and (pos_0[1]+i[1]) < 3:
                    # create a node with the passed in nodes's state, and +1 for depth
                    to_add_node = Node([[j for j in l] for l in node.state], node.depth+1, node.depth+1)
                    temp = to_add_node.state[pos_0[0]+i[0]][pos_0[1]+i[1]]
                    to_add_node.state[pos_0[0]+i[0]][pos_0[1]+i[1]] = 0
                    to_add_node.state[pos_0[0]][pos_0[1]] = temp
                    # the above 3 lines swap the values of the zero, pos_0, and the possible valid slots

                    # If we deal with duplicates here, we have less nodes expanded
                    # but it takes longer, thats okay, we are looking at the count
                    if to_add_node in self.seen_set:
                        print("already seen this expansion, not adding it to queue")
                    else:
                        to_ret.append(to_add_node)
                        self.seen_set.add(to_add_node)

        # if we did not find any unseen expansions
        # return nothing
        if len(to_ret) == 0:
            return []

        # increment our total expanded nodes cost
        self.num_exp += len(to_ret)
        return to_ret

    def queueing_function(self, nodes: List[Node], expansions: List[Node]):
        if self.algo_choice == 1:
            # print("Using Uniform Cost Search")
            # since everything costs the same, we just add the 
            # expansions to the nodes and return
            for i in expansions:
                nodes.append(i)

            print("Best node with g(n)=", nodes[0].depth, "and h(n)=",nodes[0].score - nodes[0].depth)
            nodes[0].print()
            return nodes

        if self.algo_choice == 2:
            # print("Using A* with misplaced tile heuristic")

            to_ret = []
            for exp in expansions:
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
                # score : f(n) = g(n) + h(n)
                # g(n) is the _cost to_ aka the depth, already assigned in the expansion
                # h(n) is the heuristic score, aka the manhattan or misplaced
                # so we just add h(n) to g(n) and be done!
                exp.score += misplaced_sum
                to_ret.append(exp)

            # sort expansions by misplaced tiles, smallest first
            # used this https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
            # if we do NOT want to break ties, uncomment the following line and comment line 203
            # to_ret.sort(key=lambda x: x.score)
            for i in to_ret:
                nodes.append(i)
            # to BREAK ties, uncomment the following line
            # source used: https://stackoverflow.com/questions/4233476/sort-a-list-by-multiple-attributes
            nodes.sort(key=lambda x: (x.score, x.depth))
            print("Best node with g(n)=", nodes[0].depth, "and h(n)=",nodes[0].score - nodes[0].depth)
            nodes[0].print()

            return nodes

        if self.algo_choice == 3:
            # print("Using A* with manhattan distance heuristic")

            to_ret = []
            third = [2,0,1] # needed for mapping elemnts to their goal state positions
            # Its column position is the number mod the length
            # this is because of 0 indexing, so instead of having [0,1,2],
            # everything is shifted off by one, since 0 is our blank, and 1 is the top left of the goal
            # so we shift everything over one to the right and get [2,0,1]
            for exp in expansions:
                if exp.state == self.goal_state.state:
                    print("Found goal state in queueing, returning!")
                    return [exp]

                manhattan_d = 0
                # for each square in the state, we find how far from its goal state square it is
                # each number's distance is summed and that is assgined as the nodes score  
                for i in range(0,len(exp.state)):
                    for j in range(0,len(exp.state[0])):
                        # this took a while to figure out, but it maps numbers [1,8] to their respective position in the goal state!
                        if exp.state[i][j] != 0:
                            # len(exp.state[0]) == 3 for 8 puzzle
                            r = ((exp.state[i][j] - 1)// len(exp.state[0]))      # gets the row of the i,j in the goal state
                            c = third[ (exp.state[i][j] % len(exp.state[0])) ]   # gets the column of the i,j in the goal state
                            # take the difference between the goal and current positions, that is the distance, similar to distance formula from math class!
                            manhattan_d += ( abs(r-i) + abs(c-j) )
                # score is already assigned to depth
                # score = f(n) = g(n) + h(n)
                # g(n) is the _cost to_ aka the depth
                # h(n) is the heuristic score, aka the manhattan or misplaced
                # so we just add h(n) to g(n) and be done!
                exp.score += manhattan_d
                to_ret.append(exp)

            # sort list of nodes by score
            # used this https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
            # if we do NOT want to break ties, uncomment line 203 and comment line 210
            # to_ret.sort(key=lambda x: x.score)
            for i in to_ret:
                nodes.append(i)
            # to BREAK ties, uncomment line 210 and comment line 203
            # source used: https://stackoverflow.com/questions/4233476/sort-a-list-by-multiple-attributes
            # sort by a tuple of (f(n), g(n)), if we have a tie for heuristic, 
            # we want to break it by picking the smaller depth
            nodes.sort(key=lambda x: (x.score, x.depth))

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

    nodes = problem.make_queue(problem.make_node())
    start = time.time()
    max_num_nodes = -1
    
    # how many times did we call expand()
    exp_num = 0
    num_nodes = 0
    while True:
        if len(nodes) == 0:
            return "No Solution :("

        # if the current queue size is larger than prev, use that
        max_num_nodes = max( [ len(nodes),max_num_nodes ] )
        curr_node = nodes[0]
        num_nodes += 1
        nodes = nodes[1:]
        problem.seen_set.add(curr_node)

        if curr_node.state == problem.goal_state.state:
            end = time.time()
            problem.print_algo()
            print("Found solution at depth", curr_node.depth)
            print("Total number of expanded nodes (total number of unique child nodes):", problem.num_exp)
            print("Total times nodes expanded (same as expand() calls):", exp_num)
            print("Total number of seen nodes (same as visited):",num_nodes)
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
        exp_num += 1
    return "No solution"
    # this return is never reached but here because we should have one after the loop anyway
