#!/usr/bin/env python
""" pygame.examples.moveit

This is the full and final example from the Pygame Tutorial,
"How Do I Make It Move". It creates 10 objects and animates
them on the screen.

It also has a separate player character that can be controlled with arrow keys.

Note it's a bit scant on error checking, but it's easy to read. :]
Fortunately, this is python, and we needn't wrestle with a pile of
error codes.
"""
import os
import pygame as pg
from enum import Enum

main_dir = os.path.split(os.path.abspath(__file__))[0]

# Height and Width of screen
WIDTH = int(640)
HEIGHT = int(480)
# Height and width of the sprite
SPRITE_WIDTH = int(10)
SPRITE_HEIGHT = int(10)

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Block(pg.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
       # Call the parent class (Sprite) constructor
       pg.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pg.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.speed = 10
       self.direction = Direction.RIGHT

    def get_pos(self):
        return (self.rect.x, self.rect.y)

    def moveByDirection(self):
        if self.direction == Direction.RIGHT:
            self.rect.right += self.speed
        elif self.direction == Direction.LEFT:
            self.rect.right -= self.speed
        elif self.direction == Direction.DOWN:
            self.rect.top += self.speed
        elif self.direction == Direction.UP:
            self.rect.top -= self.speed
        
        if self.rect.right > WIDTH or self.rect.top > HEIGHT - SPRITE_HEIGHT or self.rect.right < SPRITE_WIDTH or self.rect.top < 0:
            return True
        return False


# quick function to load an image
def load_image(name):
    path = os.path.join(main_dir, "data", name)
    return pg.image.load(path).convert()


# here's the full code
def main():
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    positions = []

    p = Block(pg.Color(255, 255, 255), 10, 10)

    pg.display.set_caption("Move It!")

    # This is a simple event handler that enables player input.
    collision = False
    while not collision:
        # Get all keys currently pressed, and move when an arrow key is held.
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            p.direction = Direction.UP
        elif keys[pg.K_DOWN]:
            p.direction = Direction.DOWN
        elif keys[pg.K_LEFT]:
            p.direction = Direction.LEFT
        elif keys[pg.K_RIGHT]:
            p.direction = Direction.RIGHT
            
        collision = p.moveByDirection()
        if (collision):
            screen.fill(pg.Color(255,0,0))
        for e in pg.event.get():
            # quit upon screen exit
            if e.type == pg.QUIT:
                return
        screen.blit(p.image, p.get_pos())
        for position in positions:
            if p.rect.collidepoint(position[0], position[1]):
                print('choque')
                screen.fill(pg.Color(255,0,0))
                collision = True
        positions.append(p.get_pos())
        clock.tick(60)
        pg.display.update()
        pg.time.delay(100)


if __name__ == "__main__":
    main()
    pg.quit()