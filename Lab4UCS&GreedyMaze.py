# -*- coding: utf-8 -*-
"""
@author: Christopher Chang, Drew Finch
"""

import copy
import fileinput

class node:
    def __init__(self, pos, parent):
        self.pos = pos
        self.parent = parent
        self.nextLeaf = 0           #used for tree search

start = (2,7)
goal = (7,7)
# start = (2,2)
# goal = (3,3)
fringe = [node(start, None)]
closed = []

directionPriority = [[(0,-1),(1,0),(0,1),(-1,0)], #left, down, right, up; default
                     [(-1,0),(0,1),(1,0),(0,-1)], #up, right, down, left
                     [(0,1),(-1,0),(0,-1),(1,0)], #right, up, left, down
                     [(1,0),(0,-1),(-1,0),(0,1)]] #down, left, up, right; if you want to change the dir. prior. then look for the successor functions where they add tuples and change the number in the first bracket to 0-3

maze = [[1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,0,0,0,1],
        [1,0,0,0,1,0,0,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,1,0,0,1],
        [1,1,1,0,0,1,0,0,1],
        [1,1,1,0,0,1,1,1,1],
        [1,1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1]]

# maze = [[1,1,1,1,1,1,1,1,1],
#         [1,0,0,0,1,0,0,0,1],
#         [1,0,0,0,1,0,0,0,1],
#         [1,0,0,0,0,0,0,0,1],
#         [1,0,0,0,0,1,0,0,1],
#         [1,1,1,0,0,1,0,0,1],
#         [1,1,1,0,0,1,1,1,1],
#         [1,1,0,0,0,0,1,0,1],
#         [1,1,1,1,1,1,1,1,1]]

# maze = [[1,1,1,1,1],
#         [1,0,0,0,1],
#         [1,0,1,1,1],
#         [1,0,0,0,1],
#         [1,1,1,1,1]]
# Input ex: 1 1 1 1 1,1 0 0 s 1,1 0 1 1 1,1 0 0 d 1,1 1 1 1 1

mazeCpy = copy.deepcopy(maze)

####MISC FUNCTIONS-------------------------------------------------------------
###for parsing input mazes
def scanFile(file):
    global maze
    global start
    global goal
    global mazeCpy
    
    maze = []
    row = 0
    
    for line in file:
        temp = line.split(" ")
        column = 0
        
        for e in temp:
            if (e == "s"):
                start = (row, column)
                temp[column] = "0"
            elif (e == "d"):
                goal = (row, column)
                temp[column] = "0"
            
            column += 1
            
        maze.append(list(map(int, temp)))
        row += 1
        
    mazeCpy = copy.deepcopy(maze)
        
def scanInput(Input):
    global maze
    global start
    global goal
    global mazeCpy
    
    maze = []
    
    temp = Input.split(",")
        
    for i in range(len(temp)):
        temp2 = temp[i].split(" ")
        
        for j in range(len(temp2)):
            if (temp2[j] == "s"):
                start = (i, j)
                temp2[j] = "0"
            elif (temp2[j] == "d"):
                goal = (i, j)
                temp2[j] = "0"
            
        maze.append(list(map(int, temp2)))
        
    mazeCpy = copy.deepcopy(maze)

###Displaying the maze/plan
def printMaze(Maze):
    for r in range(len(Maze)):
        for c in range(len(Maze[r])):
            if ((r,c) == start):
                print("s", end=" ")
            elif ((r,c) == goal):
                print("d", end=" ")
            else:
                print(Maze[r][c], end=(" "))
        print("")
    print("")
        
def printPlan(plan):
    global maze
    
    mazePath = copy.deepcopy(maze)
    
    for e in plan:
        mazePath[e[0]][e[1]] = "+"
        
    printMaze(mazePath)
####END MISC FUNCTIONS---------------------------------------------------------

###functions for solving the maze
def inBounds(pos):
    return pos[0] >= 0 and pos[0] < len(maze) and pos[1] >= 0 and pos[1] < len(maze[0])

def onGoal(curPos):
    if (curPos == goal):
        return True
    else:
        return False
    
def extractPlan(candidate):
    cost = 0
    plan = []
    currNode = candidate
    
    while (currNode.parent != None):
        cost += 1
        plan.append(currNode.pos)
        currNode = currNode.parent
    
    plan.append(start)
    
    return (plan, cost)



def ucsSuccessor():
    candidate = fringe.pop(0)
#    print(candidate.pos)     #for Debug
    
    for x in range(4):
        leaf = tuple(map(lambda i, j: i + j, candidate.pos, directionPriority[0][x])) #adds tuples
        if (inBounds(leaf) and mazeCpy[leaf[0]][leaf[1]] == 0):
            fringe.append(node(leaf, candidate))
            mazeCpy[leaf[0]][leaf[1]] = 1
            
def greedySuccessor():
    candidate = fringe.pop(0)
#    print(candidate.pos)     #for Debug
    
    for x in range(4):
        leaf = tuple(map(lambda i, j: i + j, candidate.pos, directionPriority[0][x])) #adds tuples
        if (inBounds(leaf) and mazeCpy[leaf[0]][leaf[1]] == 0):
            fringe.append(node(leaf, candidate))
            mazeCpy[leaf[0]][leaf[1]] = 1

#BFS search from previous lab
def ucsSearch():
   return None #Stub
    
def greedySearch():
    return None #Stub
    
    
    
def main():
    ##which type of search
    #searchStrat = input("Which method of search: tree, graph, or BFS\n")
    
    ##take maze, process into machine readable
    inputMethod = input("Which type of input: manuel or file\n")
    
    if (inputMethod == "file"):
        print("Input elements should be separated by spaces and there should be one node with 's' and another with 'd' to represent start and diamond respectively")
        file = input("File name:\n")
        
        with fileinput.input(files = file) as f:
            scanFile(f)
    else:
        print("Input the maze content with the following sytnax: 1 0 0 0 1 0 0,0 0 0 0 0 0 0 ...\nThere should be one node with 's' and one node with 'd' for start and diamond respectivly")
        text = input("Input:\n")
        
        scanInput(text)
        
    print("\nMaze:")
    printMaze(maze)
    
    ##Solve Maze
    global fringe
    
    fringe = [node(start, None)]
    plan = (None, 0)
    
    # if (searchStrat.lower() == "graph"):
    #     plan = graphSearch()
    # elif (searchStrat.lower() == "bfs"):
    plan = ucsSearch()
    # else:
    #     plan = treeSearch()
    
    ##prints results
    if (plan[0] == None):
        print("No possible path was found")
    else:
        print("Path Found:")
        printPlan(plan[0])
        print("Path: {}".format([ele for ele in reversed(plan[0])]))    #reverses to show from start to finish
        print("Cost: {}".format(plan[1]))

main()