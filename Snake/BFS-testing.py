from __future__ import annotations
import datetime
import collections
# some of these types are deprecated: https://www.python.org/dev/peps/pep-0585/
from typing import Protocol, Dict, List, Iterator, Tuple, TypeVar, Optional
T = TypeVar('T')

snake =  [(160, 440), (140, 440), (120, 440), (100, 440), (80, 440), (60, 440), (40, 440), (20, 440), (20, 420), (40, 420), (60, 420), (80, 420), (100, 420), (120, 420), (140, 420), (160, 
420), (180, 420), (200, 420), (220, 420), (240, 420), (260, 420), (280, 420), (300, 420), (320, 420), (340, 420), (360, 420), (380, 420)]
snake_wall = []
snake_head = (0,0)
food = (60,80)


GRID =[]

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

GRIDSIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE

GridLocation = Tuple[int, int]
Location = TypeVar('Location')
class Graph(Protocol):
    def neighbors(self, id: Location) -> List[Location]: pass

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, x: T):
        self.elements.append(x)
    
    def get(self) -> T:
        return self.elements.popleft()

class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: List[GridLocation] = []
    
    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls
    
    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0: neighbors.reverse() # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results

def breadth_first_search(graph: Graph, start: Location, goal: Location):
    frontier = Queue()
    frontier.put(start)
    came_from: Dict[Location, Optional[Location]] = {}
    came_from[start] = None
    
    while not frontier.empty():
        current: Location = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
    
    return came_from

def draw_grid(graph, **style):
    print("___" * graph.width)
    for x in range(graph.height):
        for y in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~~~" * graph.width)

def draw_tile(graph, id, style):
    r = " . "
    if 'number' in style and id in style['number']: r = " %-2d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = " > "
        if x2 == x1 - 1: r = " < "
        if y2 == y1 + 1: r = " v "
        if y2 == y1 - 1: r = " ^ "
    if 'path' in style and id in style['path']:   r = " @ "
    if 'start' in style and id == style['start']: r = " A "
    if 'goal' in style and id == style['goal']:   r = " Z "
    if id in graph.walls: r = "###"
    return r

def reconstruct_path(came_from: Dict[Location, Location], start: Location, goal: Location) -> List[Location]:

    current: Location = goal
    path: List[Location] = []
    while current != start: # note: this will fail if no path found
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

def generateGridCoordinates(): #generates all coordinate points on the grid board, this is used to generate the starting point. 
    for i in range(int(GRID_WIDTH)):
        for j in range(int(GRID_HEIGHT)):
            GRID.append((i*GRIDSIZE,j*GRIDSIZE))

def convertToMovement(path):
    moves = []
    start = path[0]

    for i in range(1, len(path), 1):
        if path[i] == (start[0]+UP[1], start[1]+UP[0]):
            moves.append('UP')
            start = path[i]
        elif path[i] == (start[0]+DOWN[1], start[1]+DOWN[0]):
            moves.append('DOWN')
            start = path[i]
        elif path[i] == (start[0]+RIGHT[1], start[1]+RIGHT[0]):
            moves.append('RIGHT')
            start = path[i]
        elif path[i] == (start[0]+LEFT[1], start[1]+LEFT[0]):
            moves.append('LEFT')
            start = path[i]


    return moves



def bfs():
    begin_time = datetime.datetime.now()

    tmp_grid = [[0 for y in range(int(GRID_HEIGHT))] for x in range(int(GRID_WIDTH))]

    for elm in snake:
        x, y = int(elm[0]/GRIDSIZE), int(elm[1]/GRIDSIZE)
        tmp_grid[x][y]=1
        snake_wall.append((x, y))
    snake_head = snake_wall[0]
    snake_wall.pop(0)
    tmp_grid[int(snake[0][0]/GRIDSIZE)][int(snake[0][1]/GRIDSIZE)] = 2
    tmp_grid[int(food[0]/GRIDSIZE)][int(food[1]/GRIDSIZE)] = 5

    for i in tmp_grid:
        print(i)

    g = SquareGrid(int(GRID_WIDTH), int(GRID_HEIGHT))
    g.walls = snake_wall # long list, [(21, 0), (21, 2), ...]
    draw_grid(g)

    start = (int(snake[0][0]/GRIDSIZE), int(snake[0][1]/GRIDSIZE))
    print(start)
    goal = (int(food[0]/GRIDSIZE), int(food[1]/GRIDSIZE))
    parents = breadth_first_search(g, start, goal)

    path = reconstruct_path(parents, start, goal)
    print(path)
    moves = convertToMovement(path)
    print(moves)

    draw_grid(g, point_to=parents, start=start, goal=(int(food[0]/GRIDSIZE), int(food[1]/GRIDSIZE))) 


    print('Time to complete: ' + str(datetime.datetime.now() - begin_time))


bfs()


