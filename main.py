__author__ = "Yo Fodda"
__copyright__ = "Yo Madda"

from cmath import sin
from email import header
from time import sleep
from tokenize import group
import pygame as pg
from pygame.draw import *
from pygame.math import Vector2
from pygame import gfxdraw
import os
import math
from dataclasses import dataclass

pg.init()
pg.display.set_caption('Physics Thing')
screen = pg.display.set_mode((800, 800))
screen.fill((0, 0, 0))

ZVEC2 = Vector2()
V0 = 5
A = -2
GRAVITY = 0.1

balls = pg.sprite.Group()

# x = vt
# y = -0.5at^2 + vt

ATOM_IMG = pg.Surface((16, 16), pg.SRCALPHA)
# gfxdraw.aacircle(ATOM_IMG, 8, 8, 7, (0, 255, 0))
gfxdraw.filled_circle(ATOM_IMG, 8, 8, 7, (255, 100, 0))

class Ball(pg.sprite.Sprite):
    def __init__(self, dir, mag, start: Vector2) -> None:
        super().__init__()

        self.landed = False
        rot = dir * math.pi / 180
        self.vel = Vector2(
            x=mag * math.cos(rot),
            y=-mag * math.sin(rot) # weirdo coordinate system
        )

        self.image = ATOM_IMG
        self.rect = self.image.get_rect()
        self.rect.x = start.x
        self.rect.y = start.y

    def update(self, gravity: float, dt: float):
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt
        self.vel.y += gravity * dt

        # if outside screen, delete
        if not screen.get_rect().colliderect(self.rect) and screen.get_height() < self.rect.y:
            balls.remove(self)



def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pg.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

class Cannon:
    head = pg.image.load("shooter_head.png")

    def __init__(self) -> None:
        self.rot = 0. # degrees
        self.power = 10. # 0 - 1
        self.pos = Vector2(
            x=20,
            y=580,
        )
        self.shot_time = 0

    @property
    def graphical_pos(self):
        return self.pos - self.head.get_rect().center

    def angle_to(self, other: Vector2) -> float:
        return math.atan2(self.pos.y - other.y, other.x - self.pos.x) * 180 / math.pi

    def update(self, mouse_pos: tuple[int, int]):
        # find distance between self and mouse
        # 
        # use that distnace to figure out the angle and power
        # the cannon has to be at
        #
        # set rot to that (degrees)
        self.rot = self.angle_to(Vector2(mouse_pos))

    def draw(self, dst: pg.Surface):
        dst.blit(rot_center(self.head, self.rot), self.graphical_pos)

    def shoot(self):
        # this coordinate systme sucks
        pos = self.pos.copy()
        pos.y -= 10
        pos.x -= 8
        balls.add(
            Ball(self.rot, self.power, pos)
        )      
        
bg = pg.image.load("bg.png")
cannon = Cannon()
t = 0.0
clock = pg.time.Clock()
while True:
    screen.fill((0,0,0))
    t += 0.1
    for event in pg.event.get():
        if event.type == pg.QUIT:
            print("bye bye!")
            pg.display.quit()
            exit()
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            cannon.shoot()
        elif event.type == pg.MOUSEWHEEL:
            cannon.power += event.y * 0.1


    # update
    cannon.update(pg.mouse.get_pos())
    balls.update(GRAVITY, clock.get_time() / 10)

    # draw
    bg.blit(screen, (100, 100))
    pg.draw.line(screen, (0, 250, 0), (0, 600), (800, 600), 10)  # draws ground
    balls.draw(screen)
    cannon.draw(screen)
    pg.display.flip()

    clock.tick(60)