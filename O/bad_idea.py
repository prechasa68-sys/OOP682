#bad idea
class Circle:#วงกลม
    def __init__(self, radius):
        self.radius = radius

class Rectangle:#สี่เหลี่ยม
    def __init__(self, width, height):
        self.width = width
        self.height = height

def calculate_area(shape):#คำนวณพื้นที่
    if isinstance(shape, Circle):
        return 3.14 * shape.radius ** 2
    elif isinstance(shape, Rectangle):
        return shape.width * shape.height
    else:
        raise ValueError("unknown shape")