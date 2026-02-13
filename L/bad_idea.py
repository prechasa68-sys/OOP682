class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)
    def set_width(self, width):
        self.width = width
        self.height = width
    def set_height(self, height):
        self.height = height
        self.width = height

def resize_rectangle(rectangle, new_width, new_height):
    rectangle.set_width(new_width)
    rectangle.set_height(new_height)
    return rectangle.width * rectangle.height

rect = Rectangle(10, 20)
print('rectangle area:', resize_rectangle(rect, 30, 40))
square = Square(10)
print("square area:", resize_rectangle(square, 30, 30))