from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def resize(self, new_width, new_height):
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def resize(self, new_width, new_height):
        self.width = new_width
        self.height = new_height
    def area(self):
        return self.width * self.height


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def resize(self, new_width, new_height):
        self.side = new_width

    def area(self):
        return self.side * self.side


rect = Rectangle(3, 4)
rect.resize(5, 6)
print("rectangle area:", rect.area())
sq = Square(5)
sq.resize(7, 7)
print("square area:", sq.area())
