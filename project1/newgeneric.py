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

class Problem:
    def __init__(self, arr=[[],[],[]], puzzle_type=8, goal_state=[[],[],[]], algo_choice=2):
        self.init_state = Node(arr,0,0)
        self.puzzle_type = puzzle_type
        self.seen_exp = []
        self.algo_choice = algo_choice
        self.num_exp = 0
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
            return [node]
        
        self.num_exp += len(to_ret)

        return to_ret

    def queueing_function(self, nodes, expansions):
        if self.algo_choice == 1:
            print("TODO")
            for i in expansions:
                nodes.append(i)
            return nodes
        if self.algo_choice == 2:
            print("Using A* with misplaced tile heuristic")
            
            to_ret = []
            for exp in expansions:
                if exp.state == self.goal_state.state:
                    print("Found goal state in queueing, returning!")
                    return [exp]

                misplaced_sum = 0

                for i in range(0,3):
                    for j in range(0,3):
                        if exp.state[i][j] != self.goal_state.state[i][j]:
                            misplaced_sum = misplaced_sum + 1
                
                exp.score = misplaced_sum
                to_ret.append(exp)

                to_ret.sort(key=lambda x: x.score)
            
            for i in nodes:
                to_ret.append(i)

            print("to_ret")
            for i in to_ret:
                print(i.score)
                i.print()
            return to_ret
        if self.algo_choice == 3:
            print("TODO")
            return []

def generic(problem: Problem, algo_choice=2):
    if problem.init_state.state == problem.goal_state.state:
        return "Hey! The initial state is already solved!"
    # nodes = problem.make_queue(problem.make_node)
    nodes = [problem.init_state]
    tick = 0
    while True:
        if len(nodes) == 0:
            return "No Solution :("
        
        curr_node = nodes[0]
        nodes = nodes[1:]
        if curr_node.state in problem.seen_exp:
            print("seen this node, skipping")
        
        tick += 1
        problem.seen_exp.append(curr_node.state)
        
        print("Current Depth:",curr_node.depth)
        print("Looking at")
        curr_node.print()

        if curr_node.state == problem.goal_state.state:
            print("Found solution at depth", curr_node.depth)
            print("Total number of expanded nodes:", problem.num_exp)
            print("Total number of seen nodes:",len(problem.seen_exp))
            return curr_node.state
        
        if tick == 500000:
            print("Tick count of",tick,"exceeded!")
            return "took too long"

        if curr_node.depth > 60:
            print("depth of",curr_node.depth,"and no solution, quitting")
            return "too far down without a solution"

        nodes = problem.queueing_function(nodes, problem.expand(curr_node,curr_node.operators))
    return "No solution"
