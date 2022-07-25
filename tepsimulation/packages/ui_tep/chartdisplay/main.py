import sys
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

try:
    from .display_settings import *
except ImportError:
    # For when this package is run as a script for debugging
    from display_settings import *


VIEWPORT_OBJECTS = []


def init():
    global AXRNG, AXRNG_DEFAULT
    global XOFFSET, YOFFSET

    XOFFSET = 0
    YOFFSET = 0
    AXRNG = AXRNG_DEFAULT
    updateDisplay()
    glutPostRedisplay()

    glClearColor(*COLORS_RGBA['white'])


def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glPushMatrix()

    glLineWidth(1.0)
    glPointSize(10.0)
    for obj in VIEWPORT_OBJECTS:
        obj.draw()

    glPopMatrix()
    glFlush()


def plotPoints(plot_type, point_list):
    glBegin(plot_type)
    for x, y in point_list:
        glVertex2f(x, y)
    glEnd()


def idle():
    global REFRESH_RATE
    time.sleep(1 / REFRESH_RATE)
    glutPostRedisplay()


def zoomIn():
    zoom(1/1.1)


def zoomOut():
    zoom(1.1)


def zoom(factor=1.0):
    global AXRNG, AXRNG_MIN, AXRNG_MAX
    new_axrng = AXRNG * factor
    if new_axrng < AXRNG_MIN:
        AXRNG = AXRNG_MIN
    elif new_axrng > AXRNG_MAX:
        AXRNG = AXRNG_MAX
    else:
        AXRNG = new_axrng


def keyboard(key, x, y):
    global VIEWPORT_WIDTH, VIEWPORT_HEIGHT, WINDOW
    global XOFFSET, YOFFSET, AXRNG
    if key == b'\x1b' or key == b'q':
        glutDestroyWindow(WINDOW)
    if key == b'a':
        XOFFSET += 0.1
    if key == b'd':
        XOFFSET -= 0.1
    if key == b'w':
        YOFFSET -= 0.1
    if key == b's':
        YOFFSET += 0.1
    if key == b'z':
        zoomIn()
    if key == b'x':
        zoomOut()
    if key == b'e':
        init()
    if key == b'l':
        print(f'Offset: ({XOFFSET:.3f}, {YOFFSET:.3f})\nZoom: {AXRNG:.3f}')
    if key == b'n':
        sqr = Square(-1, -1, 2, 2, COLORS_RGB['black'], COLORS_RGB['blue'])
        sqr.active = True
        VIEWPORT_OBJECTS.append(sqr)
    if key == b'm':
        VIEWPORT_OBJECTS.pop(-1)
    updateDisplay()


def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        shape = findTopShape(*mousePosOrtho(x, y))
        if shape is not None:
            shape.active = not shape.active


def mousePosOrtho(x, y):
    global VIEWPORT_WIDTH, VIEWPORT_HEIGHT
    global PROJECTION_COORDS
    x_rng = PROJECTION_COORDS[1] - PROJECTION_COORDS[0]
    y_rng = PROJECTION_COORDS[3] - PROJECTION_COORDS[2]

    x_norm = x / VIEWPORT_WIDTH
    y_norm = y / VIEWPORT_HEIGHT

    x_ortho = x_norm * x_rng + PROJECTION_COORDS[0]
    y_ortho = y_norm * y_rng + PROJECTION_COORDS[2]
    return(x_ortho, y_ortho)


def findTopShape(x, y):
    for shape in VIEWPORT_OBJECTS:
        if shape.touching(x, y):
            return(shape)
    return(None)


def updateDisplay():
    global VIEWPORT_WIDTH, VIEWPORT_HEIGHT
    reshape(VIEWPORT_WIDTH, VIEWPORT_HEIGHT)


def reshape(w, h):
    global VIEWPORT_WIDTH, VIEWPORT_HEIGHT
    global XOFFSET, YOFFSET, AXRNG
    global PROJECTION_COORDS

    h = max(h, 1)
    VIEWPORT_WIDTH = w
    VIEWPORT_HEIGHT = h

    glViewport(0, 0, VIEWPORT_WIDTH, VIEWPORT_HEIGHT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    aspect = VIEWPORT_WIDTH / VIEWPORT_HEIGHT
    if VIEWPORT_WIDTH <= VIEWPORT_HEIGHT:
        PROJECTION_COORDS = (XOFFSET - AXRNG,
                             XOFFSET + AXRNG,
                             YOFFSET - AXRNG / aspect,
                             YOFFSET + AXRNG / aspect)
    else:
        PROJECTION_COORDS = (XOFFSET - AXRNG * aspect,
                             XOFFSET + AXRNG * aspect,
                             YOFFSET - AXRNG,
                             YOFFSET + AXRNG)
    gluOrtho2D(*PROJECTION_COORDS)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    global VIEWPORT_WIDTH, VIEWPORT_HEIGHT, WINDOW
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowPosition(100, 100)
    glutInitWindowSize(VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
    WINDOW = glutCreateWindow("graph")
    glutDisplayFunc(draw)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutReshapeFunc(reshape)
    init()
    glutMainLoop()


class Square:
    def __init__(self, x: float, y: float, dx: float, dy: float,
                 color: tuple, alt_color: tuple) -> None:
        self.x = x
        self.dx = dx
        self.y = y
        self.dy = dy
        self.color = color
        self.alt_color = alt_color
        self.build_coords()
        self.active = False

    def build_coords(self) -> None:
        self.coords = [(self.x, self.y),
                       (self.x + self.dx, self.y),
                       (self.x + self.dx, self.y + self.dy),
                       (self.x, self.y + self.dy)]

    def touching(self, x, y):
        in_x_rng = self.x < x < (self.x + self.dx)
        in_y_rng = self.y < y < (self.y + self.dy)
        return(in_x_rng and in_y_rng)

    def draw(self) -> None:
        glColor3f(*self.color)
        plotPoints(GL_QUADS, self.coords)
        if self.active:
            glColor3f(*self.alt_color)
            plotPoints(GL_POINTS, self.coords)


if __name__ == "__main__":
    main()
