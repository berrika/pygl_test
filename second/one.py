import numpy as np
import matplotlib.pyplot as plt


def normalize(x):
    x /= np.linalg.norm(x)
    return x

def intersect_plane(O, D, P, N):
    # Return the distance from O to the intersection of the ray (O, D) with the
    # plane (P, N), or +inf if there is no intersection.
    # O and P are 3D points, D and N (normal) are normalized vectors.
    denominator = np.dot(N, D)
    if np.abs(denominator) < 1e-6:
        return np.inf

    t = (np.dot(N, P) - np.dot(N, O)) / denominator
    if t < 0:
        return np.inf
    return t

def intersect_sphere(O, D, S, R):
    # Return the distance from O to the intersection of the ray (O, D) with the
    # sphere (S, R), or +inf if there is no intersection.
    # O and S are 3D points, D (direction) is a normalized vector, R is a scalar.
    # It is necessary to consider the case that the sphere's centre is not at the origin
    # H(P) = (P - S) * (P - S) - R * R = 0
    OS = O - S

    a = np.dot(D, D)
    b = 2 * np.dot(D, OS)
    c = np.dot(OS, OS) - R * R
    discriminant = b * b - 4 * a * c

    if discriminant > 0:
        d = np.sqrt(discriminant)

        t_0 = (-b + d) / (2 * a)
        t_1 = (-b - d) / (2 * a)

        if t_0 < 0:
            return np.inf
        elif t_1 < 0:
            return t_0
        else:
            return t_1
    else:
        return np.inf

def intersect_triangle(O, D, ver1, ver2, ver3):
    E1 = ver2 - ver1
    E2 = ver3 - ver1
    S = O - ver1
    S1 = np.cross(D, E2)
    S2 = np.cross(S, E1)
    n = 1.0 / (np.dot(S1, E1))
    res = np.array([np.dot(S2, E2), np.dot(S1, S), np.dot(S2, D)])
    res = n * res
    t = res[0]
    u = res[1]
    v = res[2]
    if t > 0 and 1 - u - v > 0 and v >= 0 and u >= 0:
        return t
    else: 
        return np.inf

def intersect(O, D, obj):
    if obj['type'] == 'plane':
        return intersect_plane(O, D, obj['position'], obj['normal'])
    elif obj['type'] == 'sphere':
        return intersect_sphere(O, D, obj['position'], obj['radius'])
    elif obj['type'] == 'triangle':
        return intersect_triangle(O, D, obj['pv1'], obj['pv2'], obj['pv3'])

def get_normal(obj, P):
    if obj['type'] == 'sphere':
        N = normalize(P - obj['position'])
    elif obj['type'] == 'plane':
        N = obj['normal']
    elif obj['type'] == 'triangle':
        N = normalize(caculate_normal(P, obj['pv1'], obj['pv2'], obj['pv3']))
    return N
# At any point in a triangle, the normal is explicitly calculated and its z-coordiante is assumed to be negative;
def caculate_normal(P, ver1, ver2, ver3):
    L1 = ver1 - P
    L2 = ver2 - P
    N = np.cross(L1, L2)
    if N[2] > 0:
        N[2] = -N[2]
    return N
# At any point in a triangle, the color is the barycentric interpolation of the colors assigned to the 3 vertices;
def get_color(obj, P):
    if obj['type'] == 'triangle':
        u, v = get_uv(P, obj['pv1'], obj['pv2'], obj['pv3'])
        color = (1 - u - v) * obj['cv1'] + u * obj['cv2'] + v * obj['cv3']
        return color
    color = obj['color']
    if not hasattr(color, '__len__'):
        color = color(P)
    return color

def get_uv(P, ver1, ver2, ver3):
    E1 = ver2 - ver1
    E2 = ver3 - ver1
    F = P - ver1
    u = (E2[0] * F[1] - F[0] * E2[1]) / (E2[0] * E1[1] - E1[0] * E2[1])
    v = (E1[0] * F[1] - F[0] * E1[1]) / (E1[0] * E2[1] - E2[0] * E1[1])
    return u, v

def cast_ray(rayO, rayD):
    # Find first point of intersection with the scene.
    t = np.inf
    for i, obj in enumerate(scene):
        t_obj = intersect(rayO, rayD, obj)
        if t_obj < t:
            t, obj_idx = t_obj, i

    # Return None if the ray does not intersect any object.
    if t == np.inf:
        return

    # Find the object.
    obj = scene[obj_idx]

    # Find the point of intersection on the object.
    P = rayO + rayD * t

    # Find properties of the object.
    N = get_normal(obj, P)
    color = get_color(obj, P)
    toL = normalize(L - P)

    # Start computing the color.
    color_ray = ambient

    # Lambert shading (diffuse).
    color_ray += obj.get('diffuse_c', diffuse_c) * max(np.dot(N, toL), 0) * color

    return obj, P, N, color_ray


def add_sphere(position, radius, color):
    return dict(type='sphere',
                position=np.array(position),
                radius=np.array(radius),
                color=np.array(color))


def add_plane(position, normal):
    return dict(type='plane',
                position=np.array(position),
                normal=np.array(normal),
                color=lambda P : (color_white if (int(P[0]) % 2) == (int(P[2]) % 2) else color_black))

def add_triangle(pv1, pv2 ,pv3, cv1, cv2, cv3):
    return dict(type='triangle',
                pv1 = np.array(pv1),
                pv2 = np.array(pv2),
                pv3 = np.array(pv3),
                cv1 = np.array(cv1),
                cv2 = np.array(cv2),
                cv3 = np.array(cv3))

# Image's width and height (in pixels) 500px * 500px
w, h = 500, 500

# Image's aspect ratio
r = float(w) / h

# Ranges of image coordinates (-1 <= x <= 1, -1 <= y <= 1)
# But the actual y coordinates need to be divided by the aspect ratio, why?
x_min, x_max = -1.0, 1.0
y_min, y_max = -1.0 / r, 1.0 / r

# Output image data, in RGB colors
img = np.zeros((h, w, 3))

# Camera point
O = np.array([0.0, 0.25, -1.0])

# The point in the image plane to which the camera points to (z is always 0)
# Its x and y coordinates will be updated in ray casting / tracing
# In the view coordinate system, the positive direction of z-axis is against the camera
Q = np.array([0.0, 0.0, 0.0])

# Image pixel's color (black by default, i.e. drawing nothing)
# It will be updated if the ray hits an object
color_pixel = np.zeros(3)

color_white = np.ones(3)
color_black = np.zeros(3)

# Light's position
L = np.array([5.0, 5.0, -10.0])

# Light's color (white)
color_light = np.ones(3)

# Default light parameters
ambient     = 0.05
diffuse_c   = 1.0

# List of objects
scene = [
    add_plane([0.0, -0.5, 0.0], [0.0, 1.0, 0.0]),
    add_triangle([-0.1, 0.0, 0.1], [0.1, 0.0, 0.1], [0.0, 0.2, 0.1], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]),
    add_triangle([-0.1, 0.0, 0.1], [0.0, 0.2, 0.1], [-0.2, 0.2, 0.3], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 1.0]),
    add_triangle([0.1, 0.0, 0.1], [0.0, 0.2, 0.1], [0.2, 0.2, 0.3], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 1.0])
]

# Loop through all pixels in the image
for i, x in enumerate(np.linspace(x_min, x_max, w)):
    for j, y in enumerate(np.linspace(y_min, y_max, h)):
        color_pixel[:] = 0

        Q[0] = x
        Q[1] = y
        D = normalize(Q - O)
        depth = 0
        reflection = 1.0

        rayO, rayD = O, D
        flag = cast_ray(rayO, rayD)
        if not flag:
            continue
        obj, P, N, color_ray = flag

        color_pixel = color_ray

        img[h - j - 1, i, :] = np.clip(color_pixel, 0, 1)
#name
plt.imsave('one.png', img)                                 