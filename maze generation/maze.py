import pygame
from random import choice


class Cell(pygame.sprite.Sprite):
    # Define the width and height of each cell
    w, h = 8, 8

    def __init__(self, x, y, maze):
        pygame.sprite.Sprite.__init__(self)

        # Create a surface for the cell and set its position
        self.image = pygame.Surface([self.w, self.h])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x * self.w
        self.rect.y = y * self.h

        # Store coordinates and maze information
        self.x = x
        self.y = y
        self.maze = maze

        # Calculate neighboring cells
        self.nbs = [(x + nx, y + ny) for nx, ny in ((-2, 0), (0, -2), (2, 0), (0, 2))
                    if 0 <= x + nx < maze.w and 0 <= y + ny < maze.h]

    def draw(self, screen):
        # Draw the cell on the screen
        screen.blit(self.image, self.rect)


class Wall(Cell):
    def __init__(self, x, y, maze):
        super(Wall, self).__init__(x, y, maze)
        # Fill the wall cell with black color
        self.image.fill((0, 0, 0))
        self.type = 0


class Maze:
    def __init__(self, size):
        # Calculate the width and height of the maze based on cell size
        self.w, self.h = size[0] // Cell.w, size[1] // Cell.h

        # Create a grid for the maze with walls initially
        self.grid = [[Wall(x, y, self) for y in range(self.h)] for x in range(self.w)]

    def get(self, x, y):
        # Retrieve a cell from the maze grid
        return self.grid[x][y]

    def place_wall(self, x, y):
        # Place a wall cell at a specific position in the maze
        self.grid[x][y] = Wall(x, y, self)

    def draw(self, screen):
        # Draw all cells in the maze on the screen
        for row in self.grid:
            for cell in row:
                cell.draw(screen)

    def generate(self, screen=None):
        # Create a list of unvisited cells
        unvisited = [c for r in self.grid for c in r if c.x % 2 and c.y % 2]
        cur = unvisited.pop()
        stack = []

        while unvisited:
            try:
                # Choose a random unvisited neighboring cell
                n = choice([c for c in map(lambda x: self.get(*x), cur.nbs) if c in unvisited])

                # Push the current cell onto the stack and create a path between current and chosen cell
                stack.append(cur)
                nx, ny = cur.x - (cur.x - n.x) // 2, cur.y - (cur.y - n.y) // 2
                self.grid[nx][ny] = Cell(nx, ny, self)
                self.grid[cur.x][cur.y] = Cell(cur.x, cur.y, self)
                cur = n
                unvisited.remove(n)
            except IndexError:
                if stack:
                    # Backtrack if a dead end is reached
                    cur = stack.pop()

        # Draw the whole maze after it's generated
        if screen:
            self.draw(screen)
            pygame.display.update()