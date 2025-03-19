from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random
import numpy as np

def display():
    global colors, data, rx, ry, rz
    pts = [ [data[0][1], data[0][2], data[0][0]] ]
    for i in range(6):
        x = data[0][0] + data[0][4] * math.sin((1 / 3 * math.pi  * i))
        y = data[0][1] + data[0][4] * math.cos((1 / 3 * math.pi  * i))
        p = [y, data[0][2] - data[0][3], x]
        pts.append(p)                                              # caculate each refresh
    vertices = np.array(pts)
    # Reset
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Reset the camera
    gluLookAt(0.0, 0.0, 2.0, 0.0, 0.0, -1.0, 0.0, 1.0, 0.0)        # Camera looks at the origin and uses the y-axis direction as the up-vector

    # Move and rotate, stack structure
    glRotatef(rx, 0.0, 0.0, 1.0)
    glRotatef(ry, 1.0, 0.0, 0.0)
    glRotatef(rz, 0.0, 1.0, 0.0)
    glTranslatef(-0.5, 1.5, 0.0)

    # Draw the hexagonal pyramid
    glBegin(GL_TRIANGLES)
    for i in range(6):
        glColor3fv(colors[i])
        glVertex3fv(vertices[0])
        glVertex3fv(vertices[i])
        glVertex3fv(vertices[i + 1])
    glColor3fv(colors[0])
    glVertex3fv(vertices[0])
    glVertex3fv(vertices[1])
    glVertex3fv(vertices[6])
    glEnd()
    # base in white
    glBegin(GL_POLYGON)
    glColor3f(255 / 255, 255 / 255, 255 / 255)
    glVertex3fv(vertices[1])
    glVertex3fv(vertices[2])
    glVertex3fv(vertices[3])
    glVertex3fv(vertices[4])
    glVertex3fv(vertices[5])
    glVertex3fv(vertices[6])
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
    gluPerspective(45.0, w / h, 0.01, 100.0)    # fov is 90 degrees
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def pressKey(key, x, y):
    global rx, ry, rz
    if key == b'r':
        data[0][4] += 0.01
    if key == b'h':
        data[0][3] -= 0.01
    if key == b'x':
        rx += 1.0
    if key == b'y':
        ry += 1.0
    if key == b'z':
        rz += 1.0                               # keyboard control
        
w, h = 400, 400                                 # window size
u, v = 100, 100                                 # window position
rx = ry = rz = 0
data = []
with open('pyramid-params.txt') as f:
    for line in f:
        fileds = line.split(',')
        row_data = [float(x) for x in fileds]
        data.append(row_data)                   #read data
colors = []                                   
for i in range(6):
      r = random.uniform(0, 1)     
      g = random.uniform(0, 1)
      b = random.uniform(0, 1)
      c = [r, g, b]
      colors.append(c)                           # set random colors

glutInit()
glutInitDisplayMode(GLUT_RGB |
                    GLUT_DOUBLE |
                    GLUT_DEPTH)

glutInitWindowSize(w, h)
glutInitWindowPosition(u, v) 
glutCreateWindow("Hexagonal Pyramid")            # window title
 
initRendering()

glutReshapeFunc(reshape, w, h)
glutDisplayFunc(display)
glutIdleFunc(idle)
glutKeyboardFunc(pressKey)
glutMainLoop()