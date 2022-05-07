__author__ = "Yo Fodda"
__copyright__ = "Yo Madda"

from cmath import sin
from email import header
from time import sleep
import pygame as pg
from pygame.draw import *
from pygame.math import Vector2
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

balls = pg.sprite.Group()

# x = vt
# y = -0.5at^2 + vt

class Ball:
    def __init__(self, dir, mag) -> None:
        landed = False
        self.pos = Vector2()
        self.vel = Vector2(
            x=mag * math.cos(dir),
            y=mag * math.sin(dir)
        )

    def update():
        pass

    def draw(dst: pg.Surface):
        pass


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pg.transform.rotate(image, angle )
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

class Cannon:
    head = pg.image.load("shooter_head.png")

    def __init__(self) -> None:
        self.rot = 0. # degrees
        self.power = 0. # 0 - 1
        self.pos = Vector2(
            x=0,
            y=550,
        )
        self.shot_time = 0

        self.ball = Ball()

    def angle_to(self, other: Vector2) -> float:
        return math.atan2(self.pos.y - other.y, other.x - self.pos.x)

    def update(self, mouse_pos: tuple[int, int]):
        self.rot = self.angle_to(Vector2(mouse_pos))

    def draw(self, dst: pg.Surface):
        dst.blit(rot_center(self.head, self.rot), self.pos.xy)

    def shoot(self):
        pass



def main():
    bg = pg.image.load("bg.png")
    cannon = Cannon()
    t = 0.0
    while True:
        screen.fill((0,0,0))
        t += 0.1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.display.quit()
                exit()
            if event.type == pg.MOUSEBUTTONUP:
                cannon.shoot()
        
        # update
        cannon.update(pg.mouse.get_pos())

        # draw
        bg.blit(screen, bg.get_rect().center)
        pg.draw.line(screen, (0, 250, 0), (0, 600), (800, 600), 10)  # draws ground
        cannon.draw(screen)
        pg.display.flip()
                
        
        


if __name__ == "__main__":
    main()