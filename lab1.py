
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0.8, 0.2, 0.2)
    glVertex2f(200, 200)
    i = 0
    while i < 361:
        angle = i / 180 * math.pi
        glColor3f(abs(i - 180) / 360, 0.0, 0.0)
        glVertex2f(200 + 100 * math.sin(angle), 200 + 100 * math.cos(angle))
        i += 1
    glEnd()

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
    glOrtho(0.0, w, 0.0, h, 0.0, 1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


w, h = 500, 500
u, v = 100, 100

glutInit()
glutInitDisplayMode(GLUT_RGB |
                    GLUT_DOUBLE |
                    GLUT_DEPTH)

glutInitWindowSize(w, h)
glutInitWindowPosition(u, v)
glutCreateWindow("Lab 01")

initRendering()

glutReshapeFunc(reshape, w, h)
glutDisplayFunc(display)
glutIdleFunc(idle)
glutMainLoop()