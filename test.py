import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import random

# Initialize Pygame
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Initialize Pygame display
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
glutInit()

# Perspective settings
gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
glTranslatef(0.0, -2.0, -10)  # Adjust the position and zoom

# Generate random terrain heights
terrain_size = 5
terrain = [[random.uniform(-1, 1) for _ in range(terrain_size)] for _ in range(terrain_size)]

def draw_terrain():
    glBegin(GL_QUADS)
    for i in range(terrain_size - 1):
        for j in range(terrain_size - 1):
            glColor3fv((0, 1, 0))  # Green color for terrain
            glVertex3fv((i, terrain[i][j], j))
            glVertex3fv((i + 1, terrain[i + 1][j], j))
            glVertex3fv((i + 1, terrain[i + 1][j + 1], j + 1))
            glVertex3fv((i, terrain[i][j + 1], j + 1))
    glEnd()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glRotatef(1, 3, 1, 1)  # Rotate the terrain
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_terrain()
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
