import pygame
from random import random
from math import sqrt

Position = tuple[float, float]

INF = 9999999999

WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (55, 55, 55)
BLACK = (0, 0, 0)

WIDTH = 800
HEIGHT = 600
FPS = 60

AMOUNT = 100
DISTANCE = 5000

class Point:
    radius: int
    x: float
    y: float
    speed_x: float
    speed_y: float

    def __init__(self, pos: Position, *, speed: tuple[float, float] = None, radius: int = None):
        self.x, self.y = pos
        self.speed_x, self.speed_y = speed or [(random()-0.5)*2, (random()-0.5)*2]
        self.radius = radius or min(3, max(1, random() * 5))

    def draw(self, WINDOW: pygame.Surface):
        pygame.draw.circle(WINDOW, WHITE, self.pos(), self.radius)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x > WIDTH: self.x -= WIDTH
        if self.x < 0: self.x += WIDTH
        if self.y > HEIGHT: self.y -= HEIGHT
        if self.y < 0: self.y += HEIGHT

    def pos(self):
        return (self.x, self.y)


def get_distance(p1: Point, p2: Point, *, distance_type=None):
    available_distances = ['euclidian']
    if distance_type not in available_distances:
        distance_type = 'euclidian'
    
    if distance_type == 'euclidian':
        return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def connect(points: list[Point], WINDOW: pygame.Surface):
    for i, x in enumerate(points):
        for y in points[i+1:]:
            pygame.draw.line(WINDOW, DARK_GRAY, x.pos(), y.pos(), min(3, int(DISTANCE/max(get_distance(x, y)**2, 1/INF))))

def main():
    pygame.init()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("Sky")

    points = []
    for _ in range(AMOUNT):
        points.append(Point([random() * WIDTH, random() * HEIGHT]))

    running = True
    while running:
        CLOCK.tick(FPS)
        WINDOW.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False
    
        for p in points:
            p.update()

        connect(points, WINDOW)

        for p in points:
            p.draw(WINDOW)

        pygame.display.update()


if __name__ == '__main__':
    main()