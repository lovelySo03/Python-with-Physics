import pygame
from pygame.locals import *
from threading import Thread
import time
import numpy as np

# Constants
SCREEN_WIDTH = 800  
SCREEN_HEIGHT = 400
CAPTION = "Generate Was"
FPS = 60
BLUE = (0, 103, 247)
WHITE = (255, 255, 255)

class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.time = pygame.time.Clock()
        
        self.target_height = 300 
        self.tension = 0.025
        self.dampening = 0.020
        self.spread = 0.25
        self.height_splash = 5
        self.init_speed = 200
        self.init_position_x = 0
        self.final_position_x = SCREEN_WIDTH
        self.springs = []
        self.number_rod = self.create_number_rod()
        self.rod_width = self.create_rod_width()
        self.init_index = int(self.number_rod / self.rod_width)
        self.create_spring_list(self.rod_width)
        self.start_water_waves(self.rod_width)
        self.done = False
        self.run_game()

    def run_game(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.done = True
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONUP:
                    if self.counter.done == True:
                        pos = pygame.mouse.get_pos()
                        self.init_index = int(pos[0] / self.final_position_x * self.number_rod)
                        self.start_water_waves(self.rod_width)
            self.draw_level()
            for spring in self.springs:
                spring.draw(self.screen)
            self.time.tick(FPS)
            pygame.display.flip()

    def create_number_rod(self):
        return abs(int((self.init_position_x - self.final_position_x) / 2))

    def create_rod_width(self):
        return int((self.init_position_x + self.final_position_x) / self.number_rod)
            
    def create_spring_list(self, rod_width):
        for x in range(self.init_position_x, self.final_position_x, rod_width):
            self.springs.append(Spring(x, self.target_height, rod_width))

    def start_water_waves(self, rod_width):
        self.springs[self.init_index].speed = self.init_speed
        self.counter = Counter_Waves_Motion(self)
        self.counter.start()

    def update(self):
        self.update_waves()
        self.create_neighbour_list()
        self.update_neighbour()
        self.test_end_water_waves()

    def test_end_water_waves(self):
        count = 0
        for i in range(len(self.springs)):
            if not int(self.springs[i].speed) and not int(self.springs[i].y):
                count += 1
        if count == len(self.springs):
            self.stop_water_motion()

    def stop_water_motion(self):
        for i in range(len(self.springs)):
            self.springs[i].speed = 0
            self.springs[i].height = self.target_height
            self.springs[i].y = 0
   
    def update_waves(self):
        for i in range(len(self.springs)):
            self.springs[i].update(self.dampening, self.tension, self.target_height)

    def create_neighbour_list(self):
        self.lDeltas = list(self.springs)
        self.rDeltas = list(self.springs)

    def update_neighbour(self):
        for j in range(self.height_splash):
            for i in range(len(self.springs)):
                if i > 0:
                    self.lDeltas[i] = self.spread * (self.springs[i].height - self.springs[i - 1].height)
                    self.springs[i - 1].speed += self.lDeltas[i]
                if i < len(self.springs) - 1:
                    self.rDeltas[i] = self.spread * (self.springs[i].height - self.springs[i + 1].height)
                    self.springs[i + 1].speed += self.rDeltas[i]
            self.termine_update_neighbour()

    def termine_update_neighbour(self):
        for i in range(len(self.springs)):
            if i > 0:
                self.springs[i - 1].height += self.lDeltas[i]
            if i < len(self.springs) - 1:
                self.springs[i + 1].height += self.rDeltas[i]

    def draw_level(self):
        self.screen.fill(WHITE)


class Spring:
    def __init__(self, x, target_height, rod_width):
        self.x = x
        self.y = 0
        self.speed = 0
        self.height = target_height
        self.bottom = SCREEN_HEIGHT
        self.rod_width = rod_width

    def update(self, dampening, tension, target_height):
        self.y = target_height - self.height
        self.speed += tension * self.y - self.speed * dampening
        self.height += self.speed

    def draw(self, screen):
        pygame.draw.line(screen, BLUE, (self.x, self.height), (self.x, self.bottom), self.rod_width)

class Counter_Waves_Motion(Thread):
    def __init__(self, main):
        Thread.__init__(self)
        self.main = main
        self.time = 0
        self.max_time = 2
        self.time_sleep = 0.01
        self.done = False

    def run(self):
        while not self.done:
            self.main.update()
            self.time += self.time_sleep
            if self.time >= self.max_time:
                self.done = True
            time.sleep(self.time_sleep) 

if __name__ == "__main__":
    Main()

