import math

Field_x = 600
Field_y = 600

class Circle:
    def __init__(self, radius: int, x: int, y: int, magnitude: float, direction: float) -> None:
        self.radius = radius
        self.x = x
        self.y = y
        self.magnitude = magnitude
        self.direction = direction

    def draw(self) -> None:
        print(f"{self.x}, {self.y}")

    def reflect(self) -> None:
        pass


    def move(self, ref_x: int, ref_y: int) -> None:
        self.x += (1 * ref_x)
        self.y += (1 * ref_y)


if __name__ == "__main__":
    circle = Circle(10, 100, 100, True, True)

    direction_x = 1
    direction_y = 1

    for _ in range(2000):
        if circle.x >= Field_x or circle.x <= 0:
            direction_x *= -1
        if circle.y >= Field_y or circle.y <= 0:
            direction_y *= -1
        
        circle.draw()
        circle.move(direction_x, direction_y)
            
