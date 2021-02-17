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
