from ast import Not
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import numpy as np
import random

class Particle:
    # constructor
    def __init__(self, system, position, velocity, acceleration):
        self.is_aging = False
        self.is_alive = True

        self.life = 1.0
        self.aging = 0.01

        self.system = system
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.acceleration = np.array(acceleration)

        self.delta_time = 1.0
        self.size = 0.01

    def update(self):
        if not self.is_alive:
            return

        if not self.system.has_exploded:
            glColor3fv(self.system.color_lifting)
        else:
            color = self.system.color_exploding * self.life + self.system.color_falling * (1.0 - self.life)
            glColor3fv(color)

        glBegin(GL_QUADS)
        glVertex3f(self.position[0] - self.size, self.position[1] - self.size, self.position[2])
        glVertex3f(self.position[0] + self.size, self.position[1] - self.size, self.position[2])
        glVertex3f(self.position[0] + self.size, self.position[1] + self.size, self.position[2])
        glVertex3f(self.position[0] - self.size, self.position[1] + self.size, self.position[2])
        glEnd()

        self.velocity += self.acceleration * self.delta_time
        self.position += self.velocity * self.delta_time

        if self.is_aging:
            self.life -= self.aging

        if self.life <= 0.0:
            self.is_alive = False

class ParticleSystem:
    # constructor
    def __init__(self, num_particles, location, color_lifting, color_exploding, color_falling):
        self.particles = []
        self.num_particles = num_particles
        self.color_lifting = np.array(color_lifting)
        self.color_exploding = np.array(color_exploding)
        self.color_falling = np.array(color_falling)
        self.is_active = True
        self.has_exploded = False

        for i in range(self.num_particles):
            particle = Particle(self, location, [0.0, 0.05, 0.0], [0.0, -0.001, 0.0])
            self.particles.append(particle)

    def update(self):
        if not self.is_active:
            return

        if not self.has_exploded:
            first_particle = self.particles[0]
            first_particle.update()

            if np.linalg.norm(first_particle.velocity) <= 0.0001:
                for i in range(self.num_particles):
                    particle = self.particles[i]
                    particle.is_aging = True
                    particle.position = np.array(first_particle.position)
                    particle.velocity = np.array([np.random.uniform(-0.05, 0.05), np.random.uniform(-0.05, 0.05), 0.0])

                self.has_exploded = True

        else:
            self.is_active = False

            for i in range(self.num_particles):
                particle = self.particles[i]

                if particle.is_alive:
                    particle.update()

                    if not self.is_active:
                        self.is_active = True

def display():
    if paused == False:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        gluLookAt(0.0, 0.0, 1.0, 0.0, 0.0, -1.0, 0.0, 1.0, 0.0)

        for obj in container:
            obj.update()

        glutSwapBuffers()


def idle():
    display()


def initRendering():
    glEnable(GL_DEPTH_TEST)
    # glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)


def reshape(w, h):
    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90.0, w / h, 0.01, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def pressKey(key, x, y):
    # When the key S is pressed, the program toggles between being paused and simulating.
    if key == b's':
        global paused
        if paused == False:
            paused = True
        elif paused == True:
            paused = False
    # When the key F is pressed, the program creates a firework with a randomized location on the x-y plane and a randomized exploding color, and then simulates it.
    if key == b'f':
        global container
        newfire = ParticleSystem(100,
                          [random.uniform(-1,1), -0.5, -0.5],
                          [1.0, 1.0, 1.0],
                          [random.random(), random.random(), random.random()],
                          [0.0, 0.0, 0.0])
        container.append(newfire)
# The window application's size is (500, 500), and its upper-left corner is at (100, 100) on the screen;
w, h = 500, 500
u, v = 100, 100
paused = False

firework = ParticleSystem(100,
                          [random.random(), -0.5, -0.5],
                          [1.0, 1.0, 1.0],
                          [random.random(), random.random(), random.random()],
                          [0.0, 0.0, 0.0])
container = []
container.append(firework)

glutInit()
glutInitDisplayMode(GLUT_RGB |
                    GLUT_DOUBLE |
                    GLUT_DEPTH)

glutInitWindowSize(w, h)
glutInitWindowPosition(u, v)
glutCreateWindow("Fireworks")

initRendering()

glutReshapeFunc(reshape, w, h)
glutDisplayFunc(display)
glutIdleFunc(idle)
glutKeyboardFunc(pressKey)
glutMainLoop()