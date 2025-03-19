from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time
import numpy as np

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glBegin(GL_LINES) 
    glColor3f(255 / 255, 255 / 255, 255 / 255)    #white
    glVertex2f(300, 0.0)
    glVertex2f(300, 600)
    glVertex2f(0.0, 300)
    glVertex2f(600, 300)
    glVertex2f(300, 600)
    glVertex2f(285, 585)
    glVertex2f(300, 600)
    glVertex2f(315, 585)
    glVertex2f(600, 300)
    glVertex2f(585, 309)
    glVertex2f(600, 300)
    glVertex2f(585, 291)
    glEnd()                                        # axes and arrows

    glBegin(GL_LINE_STRIP) 
    glColor3f(253 / 255, 253 / 255, 150 / 255)     # yellow

    x_min = -4
    x_max = 4
    y_max = 4                                      # set x and y in right ranges
    global A
    global B
    B = B + 0.01                                   # each refresh plus 0.01
    i = x_min
    while i < x_max + 0.01:
        x = i
        rad = (x + B) / 3 * math.pi                # set B to curve and set T
        y = A * math.sin(rad) * y_max              # set A to curve
        point = np.array([  [x],
                            [y],
                            [1]   ])
        point = np.matmul(transform_Component, point)
        glVertex2f(point[0], point[1])
        i += 0.01
    glEnd()
    
    glutSwapBuffers()


def idle():
    display()


def initRendering():
    glEnable(GL_DEPTH_TEST)


def reshape(w, h):
    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, w, 0.0, h, 0.0, 1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


w, h = 600, 600                                              # window size 
u, v = 250, 250                                              # window position
A = random.uniform(1.0, 2.0)                                 # set A in right range and define A out of display to prevent value changes while drawing
B = 0.0                                                      # initialize B 
transform_Component = np.array([   [ 75,     0,  300],
                                     [ 0, 75 / 2,  300],
                                     [ 0,      0,    1]   ]) # use matrix to reshape curve


glutInit()
glutInitDisplayMode(GLUT_RGB |
                    GLUT_DOUBLE |
                    GLUT_DEPTH)

glutInitWindowSize(w, h)                             
glutInitWindowPosition(u, v)
glutCreateWindow("Animated Sine Curve")                     # window name

initRendering()

glutReshapeFunc(reshape, w, h)
glutDisplayFunc(display)
glutIdleFunc(idle)
glutMainLoop()