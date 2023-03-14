import pygame as pg
from pygame import Surface, Vector2
from random import randint
import sys


class Bonsai:
    def __init__(self, angle=60, age_factor=15, life=70, animated=False) -> None:
        self.angle = angle
        self.age_factor = age_factor
        self.life = life
        self.animated = animated

    def grow_branch(self, life: int, prev: Vector2, direction: Vector2) -> None:
        if self.animated:
            pg.time.wait(10)
            pg.display.flip()

        if life <= 4:
            self.draw_leaves(25*max(1,life), prev)
            return
        
        pg.draw.line(self.surface, pg.Color(138,54,15), prev, prev+direction*life, int(life**0.6))
        
        for i in [1,3]:
            _angle = randint(-self.angle, self.angle)
            _direction = direction.rotate(_angle)
            _life = life-randint(1,self.age_factor*i)
            self.grow_branch(life=_life, prev=prev+direction*life, direction=_direction)
    
    def draw_leaves(self, life: int, position: Vector2):
        for i in range(randint(1,life)):
            pg.draw.circle(
                surface=self.surface,
                color=pg.Color('darkgreen'),
                center=position+Vector2(randint(-25,25),randint(-5,20)),
                radius=randint(1,5)
            )

    def draw_base(self, start: Vector2) -> None:
        pg.draw.polygon(
            surface=self.surface,
            color=pg.Color('orangered2'),
            points=[
                start + Vector2(45, 0),
                start + Vector2(55, -50),
                start + Vector2(-55, -50),
                start + Vector2(-45, 0)
            ]
        )

    def generate(self, surface: Surface, start: Vector2):
        self.surface = surface
        self.draw_base(start)
        self.grow_branch(self.life, start+Vector2(0, -50), Vector2(0, -1))
        self.draw_base(start)


if __name__ == '__main__':
    window = pg.display.set_mode((800, 600))
    pg.display.set_caption('Bonsai')

    bonsai = Bonsai(animated=('-a' in sys.argv))
    bonsai.generate(window, Vector2(400, 550))

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                window.fill(pg.Color('black'))
                bonsai.generate(window, Vector2(400, 550))
                pg.event.get()
                break
        pg.display.flip()

