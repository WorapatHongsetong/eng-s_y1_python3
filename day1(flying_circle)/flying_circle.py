import pygame
import sys
import math
import random

class Circle:
    """
    Require: math
    """
    
    def __init__(self, 
                 radius: int, 
                 x: float, 
                 y: float, 
                 magnitude: float = 1, 
                 direction: float = math.pi/4):
        
        self.radius = radius
        self.x = x
        self.y = y
        self.magnitude = magnitude
        self.direction = direction

    def __eq__(self, other) -> bool:
        if self.radius == other.radius \
            and self.x == other.x \
            and self.y == other.y \
            and self.magnitude == other.magnitude \
            and self.direction == other.direction:

            return True
        
        else:
            return False

    def reflect_angle(self, normal_vector: float, funny:bool = False) -> None:
        direction_ex = (math.cos(self.direction), math.sin(self.direction))
        normal_vector_ex = (math.cos(normal_vector), math.sin(normal_vector))
        
        dot_product = (direction_ex[0] * normal_vector_ex[0])\
             + (direction_ex[1] * normal_vector_ex[1])
        
        reflected = (
            direction_ex[0] - 2 * dot_product * normal_vector_ex[0],
            direction_ex[1] - 2 * dot_product * normal_vector_ex[1]
        )
        
        self.direction = math.atan2(reflected[1], reflected[0])

        if funny:
            self.direction * math.sin(self.direction)

        self.x += self.magnitude * math.cos(self.direction)
        self.y += self.magnitude * math.sin(self.direction)

    def move(self) -> None:
        self.x += self.magnitude * math.cos(self.direction)
        self.y += self.magnitude * math.sin(self.direction)

    # def draw(self, surface, color) -> None:
    #     center = (int(self.x), int(self.y))
    #     pygame.draw.circle(surface, color, center, self.radius)

    def get_collision_box(self) -> tuple:
        return (self.x - self.radius, 
        self.x + self.radius, 
        self.y - self.radius, 
        self.y + self.radius)

class Game_Circle(Circle):
    """
    Require: pygame
    """

    def __init__(self, radius, color, x, y, magnitude = 1, direction = math.pi / 4):
        super().__init__(radius, x, y, magnitude, direction)
        self.color = color
    
    def draw(self, surface) -> None:
        center = (int(self.x), int(self.y))
        pygame.draw.circle(surface, self.color, center, self.radius)

    def bounce_edge(self, bound_x: tuple, bound_y: tuple) -> None:
        if self.get_collision_box()[0] < bound_x[0]:
            self.reflect_angle(math.pi)
        if self.get_collision_box()[1] > bound_x[1]:
            self.reflect_angle(0)
        if self.get_collision_box()[2] < bound_y[0]:
            self.reflect_angle(math.pi / 2)
        if self.get_collision_box()[3] > bound_y[1]:
            self.reflect_angle(3 * math.pi / 2)

def violently_collision(circle1: Circle, circle2: Circle) -> None:
    distance = int(math.sqrt((circle1.x - circle2.x) ** 2 + (circle1.y - circle2.y) ** 2))
    radial_sum = int(circle1.radius + circle2.radius)

    if abs(distance) < radial_sum:
        circle1.reflect_angle(circle2.direction)
        circle2.reflect_angle(circle1.direction)




pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flying Circle")

clock = pygame.time.Clock()





# Hey Serhii, Play with this Args...
circles = []

for i in range(50):
    circles.append(Game_Circle(random.randint(5, 10),
            (random.randint(0,255), random.randint(0,255), random.randint(0,255)),
            random.randint(0, SCREEN_WIDTH),
            random.randint(0, SCREEN_HEIGHT),
            random.randint(5,10),
            random.choice([1, 1.5, 4, 6, 3]))
        )

circles = tuple(circles)







running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    for element in circles:

        element.draw(screen)

        element.move()

        element.bounce_edge((0, SCREEN_WIDTH), (0, SCREEN_HEIGHT))

        for extra_circle in circles:
            if not element.__eq__(extra_circle):
                violently_collision(element, extra_circle)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()