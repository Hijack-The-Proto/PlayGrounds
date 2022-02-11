from turtle import Shape
import pygame
import sys


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 720
FPS = 30

X = 'x'
O = 'o'


class board():
    def __init__(self):
        self.position = (0,0)
        self.color = (255,255,255)
        self.board_shapes = [ #define the position and shape of the board
            [(175,262),(10,350)],
            [(294,262),(10,350)],
            [(65,372),(350,10)],
            [(65,493),(350,10)],
        ]
        self.plays = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ]
        self.positions = [
            [(0,0),(0,1),(0,2)],
            [(1,0),(1,1),(1,2)],
            [(2,0),(2,1),(2,2)]
        ]

    def draw(self, surface):
        for p in range(len(self.board_shapes)):
            r = pygame.Rect(self.board_shapes[p][0], self.board_shapes[p][1])
            pygame.draw.rect(surface, self.color, r)
        for a in range(len(self.plays)):
            for b in range(len(self.plays[0])):
                if self.plays == X:
                    pass
                elif self.plays == O:
                    pass
                else:
                    pass

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        return

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    surface.fill((45,45,45))
    score = 0
    myfont = pygame.font.SysFont("monospace", 16)
    board_state = board()


    while True:
        clock.tick(FPS)
        board_state.handle_keys()
        surface.fill((45,45,45))



        board_state.draw(surface)


        screen.blit(surface, (0,0))
        text = myfont.render('Wins: {0}'.format(score), 1, (255,255,255))
        screen.blit(text, (5, 10))
        pygame.display.update()

    return


if __name__ == '__main__':
    main()