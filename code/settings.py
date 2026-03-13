import pygame
from pytmx.util_pygame import load_pygame
from importlib import import_module
from os import walk
from os.path import join

# Game

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
TILE_SIZE = 64
FRAMERATE = 60
BG_COLOR = "#fcdfcd"

# Player

GRAVITY = 15
SPEED = 500
BULLET_SPEED = 850
JUMP_VELOCITY = -9
SHOOT_COOLDOWN_MS = 350

# Game Classes and Functions

from timer import *
from support import *
from groups import *
from sprites import *
from enemies import *
from player import *