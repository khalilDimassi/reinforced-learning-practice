import os
from maze import *
from player import Player
import pygame
from pygame.locals import *

WINSIZE = (Cell.w * 161, Cell.h * 81)


def draw_maze(screen):
    maze = Maze(WINSIZE)
    maze.generate(screen)


def main():
    pygame.init()
    scr_inf = pygame.display.Info()
    os.environ['SDL_VIDEO_WINDOW_POS'] = '{}, {}'.format(scr_inf.current_w // 2 - WINSIZE[0] // 2,
                                                         scr_inf.current_h // 2 - WINSIZE[1] // 2)
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('Maze')
    screen.fill((0, 0, 0))

    maze = Maze(WINSIZE)
    maze.generate(screen)

    player = Player(maze)

    clock = pygame.time.Clock()

    done = False
    while not done:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = True

            # Handle player movement
            if e.type == KEYDOWN:
                if e.key == K_UP:
                    player.move(0, -Cell.h // 2)
                elif e.key == K_DOWN:
                    player.move(0, Cell.h // 2)
                elif e.key == K_LEFT:
                    player.move(-Cell.w // 2, 0)
                elif e.key == K_RIGHT:
                    player.move(Cell.w // 2, 0)

        screen.fill((0, 0, 0))
        maze.draw(screen)
        player.draw(screen)

        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    main()