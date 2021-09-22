"""
@author: Christopher Chang, Drew Finch
"""


class Node:
    def __init__(self, data, parent):
        self.parent = parent
        self.children = []
        self.data = data


def create_map():
    # map_name = input("Enter map name(try \"mazeMap.txt\"): ")
    map_name = "maze.txt"
    file = open(map_name, "r")
    maze = []
    line = []
    while 1:
        char = file.read(1)
        if not char:
            break
        elif char == '\n':
            maze.append(line)
            line = []
        else:
            line.append(char)
    if line:
        maze.append(line)
    file.close()
    return maze


def print_maze(maze):
    for line in maze:
        print()
        for character in line:
            if character != '\n':
                print(character, end=' ')
            else:
                print('', end='')
    print()


def coordinates_of(maze, value):
    for i, x in enumerate(maze):
        if value in x:
            return [i, x.index(value)]


def is_wall(maze, coordinate):
    return maze[coordinate[0]][coordinate[1]] == '-'


def moves_from(maze, coordinate):
    moves = []
    directions = [[coordinate[0] + 1, coordinate[1]],
                  [coordinate[0], coordinate[1] + 1],
                  [coordinate[0] - 1, coordinate[1]],
                  [coordinate[0], coordinate[1] - 1]]

    for direction in directions:

        if not is_wall(maze, direction):
            moves.append(direction)

    return moves


def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def greedy_search(start_state):
    robot = coordinates_of(start_state, 'R')
    goal = coordinates_of(start_state, 'D')
    root = Node(robot, "ROOT")
    fringe = [root]
    visited = [root]

    while len(fringe) > 0:

        node = fringe.pop(0)

        fringe_distances = [manhattan_distance(i.data, goal) for i in fringe]
        fringe_copy = []

        # sorts fringe by manhattan distance
        while len(fringe_distances) > 0:
            for i in range(len(fringe_distances)):
                index_of_lowest = fringe_distances.index(min(fringe_distances))
                fringe_copy.append(fringe.pop(index_of_lowest))
                fringe_distances.pop(index_of_lowest)
        fringe = fringe_copy

        if node.data == goal:
            return node

        children = moves_from(start_state, node.data)

        visited_coordinates = [i.data for i in visited]

        for child in children:
            if child not in visited_coordinates:
                child_node = Node(child, node)
                fringe.append(child_node)
                visited.append(child_node)

    return "UNSOLVABLE"


maze = create_map()
print_maze(maze)
search = greedy_search(maze)
path = []
cost = 0

while search.parent != "ROOT":
    path.append(search.data)
    if maze[search.data[0]][search.data[1]].isdigit():
        cost = cost + int(maze[search.data[0]][search.data[1]])
    search = search.parent

path.append(search.data)

path.reverse()
print("path:", path)
print("cost:", cost)
