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
    def __init__(self, state=[[],[],[]], depth=0, score=0):
        self.state = state
        self.depth = depth
        self.score = score
        self.operators = [(-1,0),(0,-1),(1,0),(0,1)]

    def find_blank(self):
        for i in range(0,3):
            for j in range(0,3):
                if self.state[i][j] == 0:
                    return (i,j)
    
    def print(self):
        print(self.state[0])
        print(self.state[1])
        print(self.state[2])
        print()

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
    def __init__(self, arr=[[],[],[]], puzzle_type=8, goal_state=[[],[],[]], algo_choice=2):
        self.init_state = Node(arr,0,0)     # inital state is a node with 0 depth and 0 score
        self.puzzle_type = puzzle_type      # determines which puzzle to sovle, right now, only 8 puzzle
        self.seen = []                      # to remove duplicates from being seen more than once
        self.seen_exp = []                  # prevents returning already seen expansions
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
        for i in operators:
            if (pos_0[0]+i[0]) > -1 and (pos_0[0]+i[0]) < 3:
                if (pos_0[1]+i[1]) > -1 and (pos_0[1]+i[1]) < 3:
                    to_add_node = Node([[j for j in l] for l in node.state],node.depth+1 ,0)
                    temp = to_add_node.state[pos_0[0]+i[0]][pos_0[1]+i[1]]
                    to_add_node.state[pos_0[0]+i[0]][pos_0[1]+i[1]] = 0
                    to_add_node.state[pos_0[0]][pos_0[1]] = temp

                    if to_add_node.state in self.seen_exp:
                        print("found one already seen expansion, not adding it to queue")
                    else:
                        to_ret.append(to_add_node)
                        self.seen_exp.append(to_add_node.state)
        
        if len(to_ret) == 0:
            return []
        
        self.num_exp += len(to_ret)
        
        return to_ret

    def queueing_function(self, nodes, expansions):
        if self.algo_choice == 1:
            print("Using Uniform Cost Search")
            # since everything costs the same, we just add the 
            # expansions to the nodes and return
            for i in expansions:
                nodes.append(i)
            return nodes

        if self.algo_choice == 2:
            print("Using A* with misplaced tile heuristic")
            
            to_ret = []
            for exp in expansions:
                if exp.state not in self.seen:
                    if exp.state == self.goal_state.state:
                        print("Found goal state in queueing, returning!")
                        return [exp]

                    misplaced_sum = 0
                    for i in range(0,3):
                        for j in range(0,3):
                            # for each misplaced tile, we add one to the score
                            if exp.state[i][j] != self.goal_state.state[i][j]:
                                misplaced_sum = misplaced_sum + 1
                
                    exp.score = misplaced_sum
                    if exp.state not in self.seen:
                        to_ret.append(exp)
                        self.seen.append(exp.state)
                    else:
                        print("Seen this state, not adding to queue")

            for i in nodes:
                to_ret.append(i)

            # sort list of nodes by score
            to_ret.sort(key=lambda x: x.score)
            return to_ret
        
        if self.algo_choice == 3:
            print("Using A* with manhattan distance heuristic")

            to_ret = []
            third = [2,0,1]
            for exp in expansions:
                if exp.state == self.goal_state.state:
                    print("Found goal state in queueing, returning!")
                    return [exp]
                
                manhattan_d = 0
                # for each square in the state, we find how far from its goal state square it is
                # each number's distance is summed and that is assgined as the nodes score
                for i in range(0,3):
                    for j in range(0,3):
                        # this took a while to figure out, but it maps numbers [0,8] to their respective position in the goal state!
                        # since python treats bools like C/C++, we can use a branchless statement to check  for 0 and add 2 in one go!
                        r = ( ((exp.state[i][j] - 1)//3) + ((exp.state[i][j] == 0)*2) ) # gets the row of the i,j in the goal state
                        c = third[ (exp.state[i][j] % 3) ]                              # gets the column of the i,j in the goal state
                        # take the difference between the goal and current positions, that is the distance, similar to distance formula from math class!
                        manhattan_d += ( abs(r-i) + abs(c-j) )
                
                exp.score = manhattan_d
                to_ret.append(exp)
                self.seen.append(exp)
            
            for i in nodes:
                to_ret.append(i)

            # sort list of nodes by score
            to_ret.sort(key=lambda x: x.score)
            return to_ret

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
    # nodes = problem.make_queue(problem.make_node)
    nodes = [problem.init_state]
    tick = 0
    start = time.time()
    max_num_nodes = -1
    while True:
        if len(nodes) == 0:
            return "No Solution :("
        
        print("number of nodes in the queue:",len(nodes))
        max_num_nodes = max( [ len(nodes),max_num_nodes ] )
        print(max_num_nodes)
        curr_node = nodes[0]
        nodes = nodes[1:]
        tick += 1
        problem.seen.append(curr_node.state)
        
        print("Current Depth:",curr_node.depth)
        print("Looking at")
        curr_node.print()

        if curr_node.state == problem.goal_state.state:
            end = time.time()
            problem.print_algo()
            print("Found solution at depth", curr_node.depth)
            print("Total number of expanded nodes:", problem.num_exp)
            print("Total number of seen nodes:",len(problem.seen))
            print("Largest queue size:",max_num_nodes)
            print("Seconds elapsed WITHOUT printing:", end-start)
            return curr_node.state
        
        if tick == 50000:
            print("Tick count of",tick,"exceeded!")
            return "took too long"

        if curr_node.depth > 100:
            print("depth of",curr_node.depth,"and no solution, quitting")
            return "too far down without a solution"

        nodes = problem.queueing_function(nodes, problem.expand(curr_node,curr_node.operators))
    return "No solution"
