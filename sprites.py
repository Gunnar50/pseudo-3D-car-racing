import random
import pygame
import math
from settings import *


def draw_quad(screen, colour, x1, y1, w1, x2, y2, w2):
    pygame.draw.polygon(screen, colour, ((x1 - w1, y1), (x2 - w2, y2), (x2 + w2, y2), (x1 + w1, y1)))


def create_lines():
    lines = []
    for i in range(ROAD_LENGTH):
        line = Line()
        line.z = i * SEGMENT_LENGTH + 0.00001  # add the 0.00001 so when the self.scale divide, it will never be 0

        if 300 < i < 700:
            line.curve = 0.5

        if i > 750:
            line.y = math.sin(i / 30) * 1500

        lines.append(line)
    return lines


class Line:
    def __init__(self):
        self.x = self.y = self.z = 0  # 3d center of line
        self.X = self.Y = self.W = 0  # 2d screen coord
        self.scale = 0
        self.curve = 0

    def project(self, cam_x, cam_y, cam_z):
        self.scale = CAMERA_DEPTH / (self.z - cam_z)
        self.X = (1 + self.scale * (self.x - cam_x)) * WIDTH / 2
        self.Y = (1 - self.scale * (self.y - cam_y)) * HEIGHT / 2
        self.W = self.scale * ROAD_WIDTH * WIDTH / 2
