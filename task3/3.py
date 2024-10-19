import math

class Shape:
    def area(self):
        raise NotImplementedError("Must implement area method")

    def perimeter(self):
        raise NotImplementedError("Must implement perimeter method")

    def compare_area(self, other):
        if self.area() > other.area():
            return "greater than"
        elif self.area() < other.area():
            return "less than"
        else:
            return "equal to"

    def compare_perimeter(self, other):
        if self.perimeter() > other.perimeter():
            return "greater than"
        elif self.perimeter() < other.perimeter():
            return "less than"
        else:
            return "equal to"

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

    def perimeter(self):
        return 4 * self.side

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

class Triangle(Shape):
    def __init__(self, a, b, c):
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Does not satisfy triangle inequality")
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self):
        return self.a + self.b + self.c

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

# User input
side = float(input("Enter the side length of the square: "))
width = float(input("Enter the width of the rectangle: "))
height = float(input("Enter the height of the rectangle: "))
while True:
    a = float(input("Enter the first side of the triangle: "))
    b = float(input("Enter the second side of the triangle: "))
    c = float(input("Enter the third side of the triangle: "))
    if a + b > c and a + c > b and b + c > a:
        break
    else:
        print("The sides do not satisfy the triangle inequality. Please re-enter.")

radius = float(input("Enter the radius of the circle: "))

# Create objects
square = Square(side)
rectangle = Rectangle(width, height)
triangle = Triangle(a, b, c)
circle = Circle(radius)

# Print area and perimeter
print("Square: Area =", square.area(), "Perimeter =", square.perimeter())
print("Rectangle: Area =", rectangle.area(), "Perimeter =", rectangle.perimeter())
print("Triangle: Area =", triangle.area(), "Perimeter =", triangle.perimeter())
print("Circle: Area =", circle.area(), "Perimeter =", circle.perimeter())

# Comparison example
print("Square vs Rectangle Area Comparison:", square.compare_area(rectangle))
print("Square vs Rectangle Perimeter Comparison:", square.compare_perimeter(rectangle))
