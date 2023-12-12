import pygame
from maze import Cell, Wall


class Player(pygame.sprite.Sprite):
    def __init__(self, maze):
        pygame.sprite.Sprite.__init__(self)

        # Create a surface for the player and set its position
        self.image = pygame.Surface([Cell.w // 2, Cell.h // 2])
        self.image.fill((255, 0, 0))  # Red color for the player
        self.rect = self.image.get_rect()

        # Set initial player position (you can adjust this based on your maze layout)
        self.rect.x = 8
        self.rect.y = 8

        # Reference to the maze for collision detection
        self.maze = maze

    def draw(self, screen):
        # Draw the player on the screen
        screen.blit(self.image, self.rect)

    def move(self, dx, dy):
        # Move the player by dx and dy
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # Check for collisions with walls
        cell_x = new_x // Cell.w
        cell_y = new_y // Cell.h
        if 0 <= cell_x < self.maze.w and 0 <= cell_y < self.maze.h:
            if not isinstance(self.maze.get(cell_x, cell_y), Wall):
                self.rect.x = new_x
                self.rect.y = new_y