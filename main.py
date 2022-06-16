import time

import pygame
from settings import *
from sprites import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.previous_time = time.time()
        self.dt = 0
        # pygame.key.set_repeat(300, 100)

    def new(self):
        self.lines = create_lines()
        self.player_position = 0
        self.player_position_x = 0

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = time.time() - self.previous_time
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # loop the road from start to finish
        while self.player_position >= ROAD_LENGTH * SEGMENT_LENGTH:
            self.player_position -= ROAD_LENGTH * SEGMENT_LENGTH
        while self.player_position < 0:
            self.player_position += ROAD_LENGTH * SEGMENT_LENGTH

        self.start_position = self.player_position // SEGMENT_LENGTH

    def draw_road(self):
        x = dx = 0  # curve offset on x axis
        camera_height = 1500 + self.lines[self.start_position].y
        max_y = HEIGHT
        for i in range(self.start_position, self.start_position + 300):
            current_line = self.lines[i % ROAD_LENGTH]
            current_line.project(self.player_position_x - x, camera_height, self.player_position - (ROAD_LENGTH * SEGMENT_LENGTH if i >= ROAD_LENGTH else 0))
            x += dx
            dx += current_line.curve

            if current_line.Y < max_y:
                max_y = current_line.Y

                previous_line = self.lines[(i - 1) % ROAD_LENGTH]

                # change colour for every 3 lines
                grass_colour = LIGHT_GREEN if (i // 3) % 2 else DARK_GREEN
                road_side_colour = WHITE if (i // 3) % 2 else BLACK
                road_colour = DARK_GREY if (i // 3) % 2 else LIGHT_GREY
                road_lines = WHITE if (i // 3) % 2 else LIGHT_GREY

                # draw the grass
                draw_quad(self.screen, grass_colour, 0, previous_line.Y, WIDTH, 0, current_line.Y, WIDTH)

                # draw the road side
                draw_quad(self.screen, road_side_colour, previous_line.X, previous_line.Y, previous_line.W * 1.2, current_line.X, current_line.Y, current_line.W * 1.2)

                # draw the road
                draw_quad(self.screen, road_colour, previous_line.X, previous_line.Y, previous_line.W, current_line.X, current_line.Y, current_line.W)

                # draw white lines on the road
                draw_quad(self.screen, road_lines, previous_line.X, previous_line.Y, previous_line.W * 0.03, current_line.X, current_line.Y, current_line.W * 0.03)

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.draw_road()
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_position += 200
        if keys[pygame.K_DOWN]:
            self.player_position -= 200
        if keys[pygame.K_RIGHT]:
            self.player_position_x += 200
        if keys[pygame.K_LEFT]:
            self.player_position_x -= 200






game = Game()
if __name__ == '__main__':
    while True:
        game.new()
        game.run()
