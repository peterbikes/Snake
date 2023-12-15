#! /usr/bin/python
# **************************************************************************** #
#                                                                 __           #
#    snake.py                                                    / _)          #
#                                                       _/\/\/\_/ /            #
#          By: pedro_mota                             _|         /             #
#      Github: github.com/peterbikes                _|  (  | (  |              #
#    Linkedin: linkedin.com/in/pedrosmpm/         /__.-'|_|--|_|               #
#                                                                              #
# **************************************************************************** #

import pygame
import sys
import time
import random
from pygame.locals import *

# tile width: 40
# multiples of 40:
mult_x = [40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480, 520, 560, 600, 640, 680, 720, 760, 800, 840, 880, 920, 960, 1000, 1040, 1080, 1120, 1160, 1200, 1240]
mult_y = [40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480, 520, 560, 600, 640, 680, 720, 760, 800, 840]

# assets 
snake_head_up = pygame.image.load("assets/images/snake_head_up")
snake_head_down = pygame.image.load("assets/images/snake_head_down")
snake_head_left = pygame.image.load("assets/images/snake_head_left")
snake_head_right = pygame.image.load("assets/images/snake_head_right")
snake_tail_vertical = pygame.image.load("assets/images/snake_tail_vertical")
snake_tail_horizontal = pygame.image.load("assets/images/snake_tail_horizontal")
wall_texture = pygame.image.load("assets/images/wall_texture")
bug = pygame.image.load("assets/images/bug")
bonus_bug = pygame.image.load("assets/images/bonus_bug")
pygame.init()
eat1 = pygame.mixer.Sound("assets/sounds/eat1")
eat2 = pygame.mixer.Sound("assets/sounds/eat2")
eat3 = pygame.mixer.Sound("assets/sounds/eat3")
eat = [eat1, eat2, eat3]
crash1 = pygame.mixer.Sound("assets/sounds/crash1")
crash2 = pygame.mixer.Sound("assets/sounds/crash2")
crash3 = pygame.mixer.Sound("assets/sounds/crash3")
crash = [crash1, crash2, crash3]

class Snake:
    def __init__(self, area):
        self.area = area
        self.dir = "up"
        self.rot = snake_head_up
        self.x = 640
        self.y = 480

    def move(self):
        if self.dir == "up":
            self.y -= 40
            self.rot = snake_head_up
        if self.dir == "down":
            self.y += 40
            self.rot = snake_head_down
        if self.dir == "left":
            self.x -= 40
            self.rot = snake_head_left
        if self.dir == "right":
            self.x += 40
            self.rot = snake_head_right

    def draw(self):
        self.area.blit(self.rot, (self.x, self.y))

class Bug:
    def __init__(self, area):
        self.x = random.choice(mult_x)
        self.y = random.choice(mult_y)
        self.area = area

    def draw(self):
        self.area.blit(bug, (self.x, self.y))

class BonusBug:
    def __init__(self, area):
        self.x = random.choice(mult_x)
        self.y = random.choice(mult_y)
        self.area = area

    def draw(self):
        self.area.blit(bonus_bug, (self.x, self.y))

class Body:
    def __init__(self, x, y, rot, area):
        self.x = x
        self.y = y
        self.rot = rot
        self.area = area
        self.dir = None

    def draw_body(self):
        if(self.rot == "up" or self.rot == "down"):
            self.dir = self.rot
            self.area.blit(snake_tail_vertical, (self.x, self.y))
        else:
            self.dir = self.rot
            self.area.blit(snake_tail_horizontal, (self.x, self.y))

class Game:
    def __init__(self):
        pygame.display.set_caption("Peter Bikes Snake Game")
        self.area = pygame.display.set_mode([1320, 920])
        self.score = 0
        self.highscore = 0
        self.body_count = []
        self.bonus_counter = 0
        self.snake = Snake(self.area)
        self.bug = Bug(self.area)
        self.bonus_bug = None
        self.bug_in_map = False

    def draw_walls(self):
        x_wall = 0
        y_wall = 0
        while(x_wall <= 1320):
            self.area.blit(wall_texture,(x_wall, y_wall))
            x_wall += 40
        x_wall = 0
        while(x_wall <= 1320):
            self.area.blit(wall_texture,(x_wall, 880))
            x_wall += 40
        while(y_wall <= 920):
            self.area.blit(wall_texture,(0, y_wall))
            y_wall += 40
        y_wall = 0
        while(y_wall <= 920):
            self.area.blit(wall_texture,(1280, y_wall))
            y_wall += 40

    def draw_body(self):
        for body in self.body_count:
            body.draw_body()

    def draw_score(self):
        self.score_string = "score: " + str(self.score)
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = self.font.render(self.score_string , True, (0, 255, 0), (0,0,128))
        self.textbox = self.text.get_rect()
        self.textbox.center = (120,20)
        self.area.blit(self.text, self.textbox)

    def update_body(self):
        i = 0
        dir = self.snake.dir
        x = self.snake.x
        y = self.snake.y
        rot = self.snake.rot

        while(i < len(self.body_count)):
            if(dir == "up"):
                y += 40
            if(dir == "down"):
                y -= 40
            if(dir == "left"):
                x += 40
            if(dir == "right"):
                x -= 40
            self.body_count[i].y = y
            self.body_count[i].x = x
            self.body_count[i].rot = dir
            dir = self.body_count[i].dir
            x = self.body_count[i].x
            y = self.body_count[i].y
            i += 1

    def draw_map(self):
        self.area.fill((0,0,0))
        self.draw_walls()
        self.snake.draw()
        if not(self.snake.x == self.bug.x and self.snake.y == self.bug.y):
            self.bug.draw()
        if(self.bonus_bug):
            if not(self.snake.x == self.bonus_bug.x and self.snake.y == self.bonus_bug.y):
                self.bonus_bug.draw()
        self.draw_body()
        self.draw_score()
        pygame.display.flip()

    def check_colision(self):
        sound = random.choice(crash)
        if(self.snake.x < 40 or self.snake.x > 1240 or self.snake.y < 40 or self.snake.y > 840):
            print("YOU LOST!")
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(sound)
            time.sleep(2)
            exit()
        i = 0
        while(i < len(self.body_count)):
            if(self.snake.x == self.body_count[i].x and self.snake.y == self.body_count[i].y):
                print("YOU LOST!")
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(sound)
                time.sleep(2)
                exit()
            i += 1

    def bug_handle(self):
        sound = random.choice(eat)
        if(self.snake.x == self.bug.x and self.snake.y == self.bug.y):
            self.score += 1
            self.bonus_counter += 1
            self.body_count.append(Body(self.snake.x, self.snake.y, self.snake.dir, self.area))
            self.bug = Bug(self.area)
            pygame.mixer.Sound.play(sound)
        if(self.bonus_counter == 5):
            self.bonus_bug = BonusBug(self.area)
            self.bonus_counter = 0
        if(self.bonus_bug and (self.snake.x == self.bonus_bug.x and self.snake.y == self.bonus_bug.y)):
            self.score += 5
            self.body_count.append(Body(self.snake.x, self.snake.y, self.snake.dir, self.area))
            pygame.mixer.Sound.play(sound)
            self.bonus_bug = None

    def run(self):
        pygame.mixer.music.load("assets/sounds/snake_song")
        pygame.mixer.music.play(-1)
        move = False
        while 1:
            self.draw_map()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        exit()
                    if move == False and (event.key == K_w or event.key == K_UP) and (self.snake.dir != "down"):
                        self.snake.dir = "up"
                        move = True
                    if move == False and (event.key == K_s or event.key == K_DOWN) and (self.snake.dir != "up"):
                        self.snake.dir = "down"
                        move = True
                    if move == False and (event.key == K_a or event.key == K_LEFT) and (self.snake.dir != "right"):
                        self.snake.dir = "left"
                        move = True
                    if move == False and (event.key == K_d or event.key == K_RIGHT) and (self.snake.dir != "left"):
                        self.snake.dir = "right"
                        move = True
            self.bug_handle()
            self.snake.move()
            move = False
            self.update_body()
            self.check_colision()
            time.sleep(.1)

game = Game()
game.run()
