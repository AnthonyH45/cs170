'''
NOTE
Please run this python script like the following
`python3 tester.py 1>depthtrace.txt`
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
problems = [
    [[1,2,3],[4,5,6],[7,8,0]], # depth 0
    [[1,2,3],[4,5,6],[0,7,8]], # depth 2
    [[1,2,3],[5,0,6],[4,7,8]], # depth 4
    [[1,3,6],[5,0,2],[4,7,8]], # depth 8
    [[1,3,6],[5,0,7],[4,8,2]], # depth 12
    [[1,6,7],[5,0,3],[4,8,2]], # depth 16
    [[7,1,2],[4,8,5],[6,3,0]], # depth 20
    [[0,7,2],[4,6,1],[3,5,8]], # depth 24
    # [[1,3,6],[],[]], # depth 31
    # [[1,3,6],[],[]], # depth 31
]
algo_choice = [1,2,3]

for p in problems:
    for a in algo_choice:
        print("Solution?",generic(Problem(p,8,0,a)))
        print("Original state",p)
        print()
    print("=================================================")
