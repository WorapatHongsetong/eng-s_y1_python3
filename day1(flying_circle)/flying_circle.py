import pygame
import sys
import math

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

    def reflect_angle(self, normal_vector: float, error:bool = False) -> None:
        direction_ex = (math.cos(self.direction), math.sin(self.direction))
        normal_vector_ex = (math.cos(normal_vector), math.sin(normal_vector))
        
        dot_product = (direction_ex[0] * normal_vector_ex[0]) + (direction_ex[1] * normal_vector_ex[1])
        
        reflected = (
            direction_ex[0] - 2 * dot_product * normal_vector_ex[0],
            direction_ex[1] - 2 * dot_product * normal_vector_ex[1]
        )
        
        self.direction = math.atan2(reflected[1], reflected[0])

        if error:
            self.direction * math.sin(self.direction)

    def move(self) -> None:
        self.x += self.magnitude * math.cos(self.direction)
        self.y += self.magnitude * math.sin(self.direction)

    # def draw(self, surface, color) -> None:
    #     center = (int(self.x), int(self.y))
    #     pygame.draw.circle(surface, color, center, self.radius)

    def get_collision_box(self) -> tuple:
        return (self.x - self.radius, self.x + self.radius, self.y - self.radius, self.y + self.radius)

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





pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flying Circle")

clock = pygame.time.Clock()





# Hey Serhii, Play with this Args...
circles = (
    Game_Circle(100, GREEN, 100, 100, 20, 3),
    Game_Circle(10, (255,255,255), 100, 100, 20, 7)
    )





running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for element in circles:

        element.draw(screen)

        element.move()

        collision_box = element.get_collision_box()

        if collision_box[0] < 0:
            element.reflect_angle(math.pi)
        if collision_box[1] > SCREEN_WIDTH:
            element.reflect_angle(0)
        if collision_box[2] < 0:
            element.reflect_angle(math.pi / 2)
        if collision_box[3] > SCREEN_HEIGHT:
            element.reflect_angle(3 * math.pi / 2)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()