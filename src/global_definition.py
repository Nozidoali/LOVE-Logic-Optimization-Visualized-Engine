import pygame
import math
import subprocess
import os
import sys
from pygame.locals import *

WHITE =         (255,   255,    255)
GRAY =          (128,   128,    128)
DARK_GRAY =     (64,    64,     64)
GREEN =         (0,     255,    0)
RED =           (255,   0,      0)
DARK_GREEN =    (0,     100,    0)
BLACK =         (0,     0,      0)
BLUE =          (0,     0,      128)
C =             (0,     255,    255)
GRID =          (105,   105,    105)
YELLOW =        (255,   255,    0)
FB =            (255,   48,     48)
PINK1 =         (255,   181,    197)
PINK =          (255,   182,    193)

VERSION = 1.0
GUI_NAME = 'Logic Optimization Visualized Engine'
AUTHOR = 'why'

'''
    signals
'''
SIG_SYS_QUIT = 0
PRINT_HELP = 1
SIG_WRITE_FILE = 2
SIG_READ_FILE = 3
SIG_OPT = 4

'''
    types
'''
TYPE_DEFAULT = -1
TYPE_GRAPH_BOX = 0
TYPE_TEXT_BOX = 1
TYPE_BUTTON = 2
TYPE_MOUSE_CURSOR = 3
TYPE_OPTIMIZER = 4