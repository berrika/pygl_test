
from tkinter import FIRST
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math                                         
import numpy as np        

def pBSpline(t, control_points):
    G = control_points.T                            # Geometry G, as the transpose of control_points
                                                    # For each point in G is a column vector

    B = np.array([  [   1, -3,  3,  -1  ],          # Spline Basis B
                    [   4,  0,  -6, 3   ],
                    [   1,  3,  3,  -3  ],
                    [   0,  0,  0,  1   ]   ]) / 6  # Don't forget to multiply a scalar 1/6

    T = np.array([  [   1           ],              # Power Basis T(t)
                    [   t           ],              # Pay attention that this a column vector
                    [   t * t       ],              # np.array([1, t, t * t, t * t * t]) is a row vector
                    [   t * t * t   ]       ])      # Row vector cannot be used here

    p = np.matmul(G, np.matmul(B, T))               # Matrix multiplication, always do it on the left           
    return p

def curvature(t, control_points):
    G = control_points.T 
    B = np.array([  [  -1,   2,  -1,  0  ],          
                    [   0,  -4,   3,  0  ],
                    [   1,   2,  -3,  0  ],
                    [   0,   0,   1,  0  ]   ]) / 2
    T = np.array([  [   1           ],             
                    [   t           ],              
                    [   t * t       ],             
                    [   t * t * t   ]       ])     
    vec = np.matmul(G, np.matmul(B, T))    
    vec_norm = np.linalg.norm(vec)
    dB = np.array([  [   1, -1,  0,  0  ],          
                    [  -2,  3,  0,  0  ],
                    [   1, -3,  0,  0  ],
                    [   0,  1,  0,  0  ]   ]) 
    dT = np.array([  [   1           ],             
                    [   t           ],              
                    [   t * t       ],             
                    [   t * t * t   ]       ])     
    if vec_norm == 0:
        vec_norm = 0.01
    K = np.matmul(G, np.matmul(dB, dT)) / vec_norm
    cur = np.linalg.norm(K)
    if cur > 5:
        cur = 5
    if cur < 0:
        cur = 0
    return cur                                         # calculate cur 

def display(): 
    c = 0                                              # control point number
    pts = []
    with open('control-points.txt') as f:
        lines = f.readlines()
        res = len(lines)
        first_line = lines[0]
        lim = 0
        fileds = first_line.split(',')
        row_data = [float(x) for x in fileds]
        while lim < res - 1:
             pts.append(row_data)
             c += 1    
             lim += 1
    with open('control-points.txt') as f:
        #read one line each time
        for line in f:
            fileds = line.split(',')
            row_data = [float(x) for x in fileds]
            pts.append(row_data)
            c += 1                        
    with open('control-points.txt') as f:
        lines = f.readlines()
        res = len(lines)
        last_line = lines[-1]
        lim = 0
        fileds = last_line.split(',')
        row_data = [float(x) for x in fileds]
        while lim < res - 1:
             pts.append(row_data)
             c += 1    
             lim += 1                     # construct control point
    pts = np.array(pts)
    n = 100                               # Number of intervals for discretizing t

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # Draw control points
    glPointSize(4.0)                      # point size 4.0
    glColor3f(0.0, 255 / 255, 0.0)        # In green

    glBegin(GL_POINTS)
    for i in range(c):              # Change 4 to the actual number of control points
        glVertex2fv(pts[i])
    glEnd()

    glPointSize(1.0)                # Always good to reset a status

    # Draw B-Spline
    glColor3f(1.0, 1.0, 1.0)        # In white
    glBegin(GL_LINE_STRIP)
    for s in range(c - 4 + 1):      # For every 4 consecutive control points
        cp = pts[s:s+4]             # Get them from pts
        for i in range(n + 1):      # Draw their part
            t = i / n
            p = pBSpline(t, cp)     # Change pts to cp
            glVertex2fv(p)
            glColor3f(curvature(t, cp) / 5, 0.0, (1 - curvature(t, cp) / 5))
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
    glOrtho(0.0, w, 0.0, h, 0.0, 1.0)           # Orthogonal projection

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


w, h = 550, 550                                 # window size
u, v = 150, 150                                 # window position

glutInit()
glutInitDisplayMode(GLUT_RGB |
                    GLUT_DOUBLE |
                    GLUT_DEPTH)

glutInitWindowSize(w, h)
glutInitWindowPosition(u, v)
glutCreateWindow("Special B-Splines")            # title

initRendering()

glutReshapeFunc(reshape, w, h)
glutDisplayFunc(display)
glutIdleFunc(idle)
glutMainLoop()
