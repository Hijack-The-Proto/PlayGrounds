from __future__ import annotations
import pygame
import sys
import random
import math
import argparse
import collections
from typing import Protocol, Dict, List, Iterator, Tuple, TypeVar, Optional

#Global Variables
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRIDSIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE

UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

FPS = 60

T = TypeVar('T')
GRIDLOCATION = Tuple[int, int]
LOCATION = TypeVar('LOCATION')

GRID = []
MOVE_QUEUE = []

class Graph(Protocol):
    def neighbors(self, id: LOCATION) -> List[LOCATION]: pass

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
        self.walls: List[GRIDLOCATION] = []
    
    def in_bounds(self, id: GRIDLOCATION) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id: GRIDLOCATION) -> bool:
        return id not in self.walls
    
    def neighbors(self, id: GRIDLOCATION) -> Iterator[GRIDLOCATION]:
        (x, y) = id
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0: neighbors.reverse() # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results


class Food(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (255, 0, 0)
        self.randomize_position([(0,0)])

    def randomize_position(self, snake): 
        tmp = [elem for elem in GRID if elem not in snake]
        self.position = random.choice(tmp)

    def draw(self, surface):
        r = pygame.Rect((self.position[0]+1, self.position[1]+1), (GRIDSIZE-2, GRIDSIZE-2))
        pygame.draw.rect(surface, self.color, r)


class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [random.choice(GRID)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.rotation = [(0,0)]
        self.new_direction = self.direction
        self.color = (0, 128, 0)
        self.initial_snake_speed = 200 # larger is slower
        self.snake_speed = self.initial_snake_speed
        self.max_length = 560 #FIX ME: make this variable depending on the amount of spaces on the board at the start of the game. 

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.new_direction = point

    def move(self, score_board):
        current = self.get_head_position()
        x, y = self.new_direction
        self.direction = self.new_direction
        new_head_position = (((current[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), (current[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new_head_position in self.positions[2:]:
            self.reset(score_board)
        else:
            self.positions.insert(0, new_head_position)
            self.rotation.insert(0, self.direction)
            if len(self.positions) > self.length:
                self.positions.pop()
                self.rotation.pop()
    def reset(self, score_board):
        self.length = 1
        score_board.score = 0
        self.snake_speed = self.initial_snake_speed
        self.positions = [random.choice(GRID)]
        self.rotation = [(0,0)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])


    def draw(self, surface): #We create two rectangles, one representing the body position, and one lagging behind by 5 pixels to fill the gaps in the snake body. this is visually more appealing. 
        for p in range(len(self.positions)):
            r = pygame.Rect((self.positions[p][0]+1, self.positions[p][1]+1), (GRIDSIZE-2, GRIDSIZE-2))
            r_lag = pygame.Rect((self.positions[p][0]+1+((self.rotation[p][0]*-1)*5), self.positions[p][1]+1+((self.rotation[p][1]*-1)*5)), (GRIDSIZE-2, GRIDSIZE-2))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, self.color, r_lag)
            #pygame.draw.rect(surface, (93,216,228), r, 1)
        
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

def breadth_first_search(graph: Graph, start: LOCATION, goal: LOCATION):
    frontier = Queue()
    frontier.put(start)
    came_from: Dict[LOCATION, Optional[LOCATION]] = {}
    came_from[start] = None
    
    while not frontier.empty():
        current: LOCATION = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
    
    return came_from

def reconstruct_path(came_from: Dict[LOCATION, LOCATION], start: LOCATION, goal: LOCATION) -> List[LOCATION]:

    current: LOCATION = goal
    path: List[LOCATION] = []
    while current != start: # note: this will fail if no path found
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

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

class Score(object):
    def __init__(self):
        self.score = 0

def drawGrid(surface): #draws a grip pattern on the background to help visualize the snakes rows and colemns 
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x+y) % 2 == 0:
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (66, 66, 66), r)
            else:
                rr = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (104, 104, 104), rr)

def create_argument_parser():
    parser = argparse.ArgumentParser(description='Snake Game. Choose what Algorythem you would like to use, or choose nothing to play Snake yourself.')
    parser.add_argument('--brute-force', help='Solves snake using a brute force approach', action='store_true', dest='bruteForce', default=False)
    parser.add_argument('--BFS', help='Trys to solve snake by using a Bredth First Search approach', action='store_true', dest='bfs_search', default=False)
    return parser

def bruteForceSearch(snake):
    snake_head = snake.get_head_position()
    #Using some hard coding of edges, will fix later using the GRIDSIZE global variables

    #This segment takes care of the base cases of movment. the snake shoudl zigzag down the screen while keeping the farthest left column open
    if 460 == snake_head[0] and snake.direction != DOWN: #Checking snake.direction lets us know what our last move was, eleminating the need for any vairables to be passed to this function
        snake.turn(DOWN)
    elif snake_head[0] > 20 and snake.direction != RIGHT:
        snake.turn(LEFT)
    if 20 == snake_head[0] and snake.direction != DOWN and snake_head[1] != 0.0: #This if check needed to ignore going down when the snake reached to top and turned right to begin the loop
        snake.turn(DOWN)
    elif 1 < snake_head[0] < 460 and snake.direction != LEFT: # the 1 < here is to let the loop ignore any movement in the 0 column while the snake returns to the top of the board.
        snake.turn(RIGHT)

    #These dictate the loop the snake takes. when the snake reaches the lewest left point in its zig zag, regardless of what row it started on, 
    #it will turn left to begin going up to restart the loop. 
    if (20.0, 460.0) == snake_head:
        snake.turn(LEFT)
    elif (0.0, 460.0) == snake_head:
        snake.turn(UP)
    elif (0.0, 0.0) == snake_head:
        snake.turn(RIGHT)
    return snake 

def searchAlgo(food, snake, args): #I need a guard in here against multiple seach algo flags being called
    if args.bruteForce:
        bruteForceSearch(snake)
    if args.bfs_search:
        breadth_first_search(snake, food)
    return snake

def generateGridCoordinates(): #generates all coordinate points on the grid board, this is used to generate the starting point. 
    for i in range(int(GRID_WIDTH)):
        for j in range(int(GRID_HEIGHT)):
            GRID.append((i*GRIDSIZE,j*GRIDSIZE))


def main():
    parser = create_argument_parser()
    args = parser.parse_args()
    generateGridCoordinates() 
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    surface.fill((45,45,45))

    snake = Snake()
    food = Food()
    score_board = Score()

    myfont = pygame.font.SysFont("monospace", 16)

    time_elapsed = 0
    while True:
        time = clock.tick(FPS)
        snake.handle_keys()
        #drawGrid(surface)
        surface.fill((45,45,45))

        time_elapsed += time
        if time_elapsed > snake.snake_speed: #Set the pace that the snake moves at so that it can be sped up as the game prgresses
            
            searchAlgo(food, snake, args)

            snake.move(score_board)
            #print(snake.positions)
            time_elapsed = 0


        if snake.get_head_position() == food.position:
            if snake.length < snake.max_length:
                snake.length+=1
            score_board.score+=1
            food.randomize_position(snake.positions)
            snake.snake_speed = math.ceil(snake.snake_speed * 0.99)

        snake.draw(surface)
        food.draw(surface)

        screen.blit(surface, (0,0))
        text = myfont.render('Score {0} {1}'.format(score_board.score, snake.snake_speed), 1, (255,255,255))
        screen.blit(text, (5, 10))
        pygame.display.update()


    return

if __name__ == '__main__':
    main()