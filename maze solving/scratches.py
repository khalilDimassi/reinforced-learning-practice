import pygame
import heapq
import time
import random


class Maze:
    def __init__(self, width, height, start, end):
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.maze = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.path = []
        self.path_finding_in_progress = False


    def generate_maze(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up
        random.shuffle(directions)
        stack = [self.start]
        while stack:
            x, y = stack[-1]
            self.maze[y][x] = 0 # Carve out a path
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and
                    self.maze[ny][nx] == 1):
                    stack.append((nx, ny))
                    break
            else:
                # If no unvisited neighbors, backtrack
                stack.pop()
        self.maze[self.end[1]][self.end[0]] = 0 # Carve out the end point


    def render_maze(self, screen):
        block_size = 20
        colors = {
            1: (0, 0, 0),      # Wall
            0: (255, 255, 255) # Path
        }

        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                color = colors.get(cell, (255, 255, 255))

                if (x, y) == self.start:
                    color = (0, 255, 0)  # Start
                elif (x, y) == self.end:
                    color = (255, 0, 0)  # End

                pygame.draw.rect(screen, color, (x * block_size, y * block_size, block_size, block_size))


    def find_path(self):
        queue = [(0, self.start)]
        distances = {self.start: 0}
        while queue:
            (cost, current) = heapq.heappop(queue)
            if current == self.end:
                break
            for neighbor in self.get_neighbors(current):
                old_cost = distances.get(neighbor, float('inf'))
                new_cost = cost + 1
                if new_cost < old_cost:
                    distances[neighbor] = new_cost
                    heapq.heappush(queue, (new_cost, neighbor))
        return self.build_path(distances)


    def animate_path(self, screen):
        for point in self.path:
            pygame.draw.rect(screen, (0, 255, 0), (point[0] * 20, point[1] * 20, 20, 20))
            pygame.display.flip()
            pygame.time.wait(100)


    def main(self, screen):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Left mouse button
                        self.generate_maze()
                    elif event.button == 3: # Right mouse button
                        self.find_path()
                        self.animate_path(screen)
            self.render_maze(screen)
        pygame.quit()

def get_neighbors(maze, node):
    neighbors = []
    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Right, Left, Down, Up
        neighbor = (node[0] + direction[0], node[1] + direction[1])
        if (0 <= neighbor[0] < len(maze[0]) and 0 <= neighbor[1] < len(maze) and
            maze[neighbor[1]][neighbor[0]] == 0): # If the neighbor is a path
            neighbors.append(neighbor)
    return neighbors

def dijkstra(maze, start, end):
    # Initialize the distance to all nodes as infinity
    distance = {point: float('inf') for row in maze for point in row}
    distance[start] = 0

    # Initialize the priority queue with the start node
    queue = [(0, start)]

    while queue:
        # Get the node with the smallest distance
        current_distance, current_node = heapq.heappop(queue)

        # If the current node is the end node, we have found the shortest path
        if current_node == end:
            return distance

        # If the current distance is greater than the recorded distance, skip this node
        if current_distance > distance[current_node]:
            continue

        # For each neighbor of the current node
        for neighbor in get_neighbors(maze, current_node):
            # Calculate the distance to the neighbor through the current node
            distance_through_current_node = current_distance + 1

            # If the distance to the neighbor through the current node is less than the recorded distance
            if distance_through_current_node < distance[neighbor]:
                # Update the recorded distance and add the neighbor to the queue
                distance[neighbor] = distance_through_current_node
                heapq.heappush(queue, (distance[neighbor], neighbor))

    # If there is no path to the end node
    return None

if __name__ == '__main__':
    pygame.init()
