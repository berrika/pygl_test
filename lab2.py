
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math                                         # Support math operations
import numpy as np                                  # Support efficient vectors and matrices

def display():
    pts = np.array([    [100, 200],
                        [150, 300],
                        [200, 200],
                        [250, 300],
                        [300, 200],
                        [350, 300],
                        [400, 200],
                        [450, 300]  ])    # Control points as a NumPy array
    c = 8                                 # Number of control points
    n = 100                               # Number of intervals for discretizing t

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Draw control points
    glPointSize(5.0)                # Default point size 1.0 is too small
    glColor3f(1.0, 0.0, 0.0)        # In red

    glBegin(GL_POINTS)
    for i in range(c):              # Change 4 to the actual number of control points
        glVertex2fv(pts[i])
    glEnd()

    glPointSize(1.0)                # Always good to reset a status

    # Draw B-Spline
    glColor3f(1.0, 1.0, 1.0)        # In white

    glBegin(GL_LINE_STRIP)
    for s in range(c - 4 + 1):      # For every 4 consecutive control points
        cp = pts[s:s + 4]             # Get them from pts
        for i in range(n + 1):      # Draw their part
            t = i / n
            p = pBezierCurve(t, cp)     # Change pts to cp
            glVertex2fv(p)
    glEnd()

    glutSwapBuffers()

def pBezierCurve(t, control_points):
    p = math.pow(1 - t, 3) *            control_points[0] + \
        3 * t * math.pow(1 - t, 2) *    control_points[1] + \
        3 * t * t * (1 - t) *           control_points[2] + \
        math.pow(t, 3) *                control_points[3]
    return p

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
glutCreateWindow("Lab 02")

initRendering()

glutReshapeFunc(reshape, w, h)
glutDisplayFunc(display)
glutIdleFunc(idle)
glutMainLoop()
