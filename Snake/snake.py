import pygame
import sys
import random
import math


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

class Food(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (223, 163, 49)
        self.randomize_position([(0,0)])

    def randomize_position(self, snake):  # FIX ME: pass in a list of locations that snake is not in. 
        self.position = (random.randint(0, GRID_WIDTH-1) * GRIDSIZE, random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)
        while self.position in snake: #this ensures that we dont put a food inside a spot ocupied by snake. this could be very slow though when snake takes up most of the board.
            self.position = (random.randint(0, GRID_WIDTH-1) * GRIDSIZE, random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93,216, 228), r, 1)


class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.new_direction = self.direction
        self.color = (17, 24, 47)
        self.initial_snake_speed = 250 # larger is slower

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.new_direction = point

    def move(self):
        current = self.get_head_position()
        x, y = self.new_direction
        self.direction = self.new_direction
        new = (((current[0] + (x*GRIDSIZE)) % SCREEN_WIDTH), (current[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])


    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0]+1, p[1]+1), (GRIDSIZE-2, GRIDSIZE-2))
            pygame.draw.rect(surface, self.color, r)
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

class Score(object):
    def __init__(self):
        self.score = 0

def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x+y) % 2 == 0:
                r = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                rr = pygame.Rect((x*GRIDSIZE, y*GRIDSIZE), (GRIDSIZE, GRIDSIZE))
                pygame.draw.rect(surface, (84, 194, 205), rr)



def main():

    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()
    score_board = Score()

    myfont = pygame.font.SysFont("monospace", 16)

    time_elapsed = 0
    snake_speed = snake.initial_snake_speed
    while True:
        time = clock.tick(FPS)
        snake.handle_keys()
        drawGrid(surface)

        print(snake.positions)

        time_elapsed += time
        if time_elapsed > snake_speed: #Set the pace that the snake moves at so that it can be sped up as the game prgresses
            snake.move()
            time_elapsed = 0
            if snake.length ==1: #A very brute force way to reset the scoreboard after death. 
                score_board.score = 0 
                snake_speed = snake.initial_snake_speed


        if snake.get_head_position() == food.position:
            snake.length+=1
            score_board.score+=1
            food.randomize_position(snake.positions)
            snake_speed = math.ceil(snake_speed * 0.99)

        snake.draw(surface)
        food.draw(surface)

        screen.blit(surface, (0,0))
        text = myfont.render('Score {0} '.format(score_board.score), 1, (0,0,0))
        screen.blit(text, (5, 10))
        pygame.display.update()


    return

if __name__ == '__main__':
    main()