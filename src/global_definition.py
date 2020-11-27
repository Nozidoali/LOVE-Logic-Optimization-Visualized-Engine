import pygame
import math
import subprocess
import os
import sys
from pygame.locals import *
# import tkinter as tk
import queue 
import time

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
PINK =          (255,   182,    193,70)
BB =            (192,   203,    216, 70)
BY =            (88,    112,    144, 110)
SB =            (129,   150,    177, 90)
OB =            (0,     35,     76, 90)
SG =            (88,    121,    146)
SpG =           (142,   146,    149)
RBF =           (13,    27,     42)
BdB =           (65,    90,     119)
Pl =            (224,   225,    221)
DS =            (224,   193,    179, 70)
PP =            (216,   154,    158, 90)
Pu =            (195,   125,    146, 70)
Gu =            (52,    58,     64, 150)
DG =            (73,    80,     87, 140)
CBC =           (173,   181,    189, 90)
Cu =            (233,   236,    239, 70)
BC =            (92,    103,    125, 90)
Ma =            (151,   157,    172, 90)

VERSION = 3.9
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
SIG_CLR = 5
SIG_AND = 6
SIG_LEN = 7
SIG_RIN = 8
SIG_LRN = 9
SIG_UNDO = 10

'''
    types
'''
TYPE_DEFAULT = -1
TYPE_GRAPH_BOX = 0
TYPE_TEXT_BOX = 1
TYPE_BUTTON = 2
TYPE_MOUSE_CURSOR = 3
TYPE_OPTIMIZER = 4
TYPE_COUNT_BOX = 5
TYPE_BENCHMARK = 6

'''
    node types
'''
NT_AND  = 0
NT_LN   = 1
NT_RN   = 2
NT_LRN  = 3

'''
    color theme
'''
COLOR_EDGE_HIGHLIGHT =  [255,   182,    193]
COLOR_EDGE_ENDANGER =   [255,   0,   0]
COLOR_EDGE_NORMAL =     [128,   128,    128]

COLOR_NODE_HIGHLIGHT =  [255,   182,    193]
COLOR_NODE_ENDANGER =   [255,   0,   0]
COLOR_NODE_NORMAL =     [255,   255,    255]
