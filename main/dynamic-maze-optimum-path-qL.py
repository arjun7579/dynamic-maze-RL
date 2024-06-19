import pygame
import numpy as np
import random
import time

# Define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 182, 193)

# Environment parameters
maze = [
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 1, 1, 0, 1, 1, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

source = [0, 0]
dest = [9, 9]
dynamic_obstacles = [(1, 1), (7, 8), (5, 5)]

# Learning parameters
alpha = 0.9  # Learning rate (0-1)
gamma = 0.9  # Discount factor (0-1)
epsilon = 0.8  # Epsilon for epsilon-greedy (0-1)
episodes = 100  # Episodes
entropy = 0.8  # Entropy for dynamic obstacles (0-1)

# Initialize Q-table
q = np.zeros((len(maze), len(maze[0]), 4))

# Define action dictionary
actions = {0: 'up', 1: 'right', 2: 'down', 3: 'left'}
inverted_actions = {v: k for k, v in actions.items()}

# Define actions function
def next_cell(action, m, n):
    if action == 'up':
        return max(m - 1, 0), n
    elif action == 'down':
        return min(m + 1, len(maze) - 1), n
    elif action == 'right':
        return m, min(n + 1, len(maze[0]) - 1)
    elif action == 'left':
        return m, max(n - 1, 0)

# Function for optimal path
def optimal_path():
    m, n = source
    path = [[m, n]]
    while [m, n] != dest:
        action = actions[np.argmax(q[m, n])]
        m, n = next_cell(action, m, n)
        path.append([m, n])
    return path

# Function to update position of dynamic obstacles
def update_maze(entropy):
    global maze, dynamic_obstacles
    
    def is_valid_position(pos):
        x, y = pos
        if x < 0 or x >= len(maze) or y < 0 or y >= len(maze[0]):
            return False
        if maze[x][y] == 1:
            return False
        if (x, y) in [obs for obs in dynamic_obstacles if obs != (x, y)]:
            return False
        return True
    
    def get_valid_neighbors(pos):
        x, y = pos
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [neighbor for neighbor in neighbors if is_valid_position(neighbor)]
    
    new_dynamic_obstacles = []
    for obstacle in dynamic_obstacles:
        valid_neighbors = get_valid_neighbors(obstacle)
        if valid_neighbors:
            scaled_entropy = int(entropy * len(valid_neighbors))
            new_obstacle = valid_neighbors[random.randint(0, scaled_entropy)]
            new_dynamic_obstacles.append(new_obstacle)
    dynamic_obstacles = new_dynamic_obstacles
    
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 2:
                maze[i][j] = 0
    for obstacle in dynamic_obstacles:
        x, y = obstacle
        maze[x][y] = 2

# Perform Q-learning
start = time.time()
for i in range(episodes):
    m, n = source
    while [m, n] != dest:
        # Epsilon-greedy action selection
        if random.random() < epsilon:
            action = random.choice(list(actions.values()))  # Random action selection
        else:
            action = actions[np.argmax(q[m, n])]  # Maximum reward action selection

        # Calculate new cell based on action
        m_new, n_new = next_cell(action, m, n)

        # Calculate reward and update Q-value
        if maze[m_new][n_new] == 1:  # Check if the new cell is an obstacle
            reward = -10  # Assign negative reward for moving into an obstacle
        elif maze[m_new][n_new] == 2:  # Checking for dynamic obstacle
            reward = -5
        else:
            reward = -1 if [m_new, n_new] != dest else 100  # Assign normal rewards otherwise

        max_q_prime = np.max(q[m_new, n_new])
        q[m, n, inverted_actions[action]] = (1 - alpha) * q[m, n, inverted_actions[action]] + alpha * (reward + gamma * max_q_prime)

        # Updating the current cell
        m, n = m_new, n_new
    update_maze(entropy)

end = time.time()
print("Time Elapsed:", end - start)

# Extracting optimal path
path = optimal_path()

# Initialize Pygame
pygame.init()

# Setting up the display
cell_size = 40
maze_width = len(maze[0]) * cell_size
maze_height = len(maze) * cell_size
screen = pygame.display.set_mode((maze_width, maze_height))
pygame.display.set_caption('Maze')

# Function to represent Maze
def draw_maze():
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if [i, j] == source:
                color = BLUE
            elif [i, j] == dest:
                color = GREEN
            elif maze[i][j] == 1:
                color = BLACK
            elif maze[i][j] == 2:
                color = RED
            else:
                color = WHITE
            pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))
    pygame.display.flip()

# Optimal path function
def draw_optimal_path():
    for cell in path[1:-1]:
        pygame.draw.rect(screen, PINK, (cell[1] * cell_size, cell[0] * cell_size, cell_size, cell_size))
    pygame.display.flip()

# Giving Output
screen.fill(WHITE)
draw_maze()
draw_optimal_path()

# To keep the window running until user closes
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
