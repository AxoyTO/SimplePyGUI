import math


class Shape:
    title = "Shape"

    def __init__(self):
        self.methods = ["Area", "Perimeter"]

    def create(self):
        pass

    def input_create(self):
        pass

    def area(self):
        pass

    def perimeter(self):
        pass

    @classmethod
    def title(cls):
        return cls.title

    @staticmethod
    def call(str):
        print("Don't call me without an instance, I'm just an abstract shape!")


class Square(Shape):
    title = "Square"

    def __init__(self):
        self.methods = ["Area", "Perimeter"]

    def create(self, side_a):
        self.side_a = side_a

    def area(self):
        return self.side_a ** 2

    def perimeter(self):
        return self.side_a * 4


class Rectangle(Square):
    title = "Rectangle"

    def create(self, a, b):
        self.side_a = a
        self.side_b = b

    def area(self):
        return self.side_a * self.side_b

    def perimeter(self):
        return (self.side_a + self.side_b) * 2


class Cube(Square):
    title = "Cube"

    def __init__(self):
        self.methods = ["Volume", "Surface Area"]

    def volume(self):
        return self.side_a * 12

    def surface_area(self):
        return 6 * self.side_a ** 2


class Parallelepiped(Rectangle):
    title = "Parallelepiped"

    def create(self, side_a, side_b, side_c):
        super().create(side_a, side_b)
        self.side_c = side_c

    def area(self):
        return 2 * (self.side_a * self.side_b + self.side_b * self.side_c + self.side_a * self.side_c)

    def perimeter(self):
        return 4 * self.side_a + 4 * self.side_b + 4 * self.side_c


class Circle(Shape):
    title = "Circle"

    def __init__(self):
        super().__init__()
        self.methods.append("Diameter")

    def create(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

    def diameter(self):
        return self.radius * 2


class Sphere(Circle):
    title = "Sphere"

    def __init__(self):
        self.methods = ["Volume", "Surface Area", "Diameter"]

    def volume(self):
        return (4 / 3) * math.pi * self.radius ** 3

    def surface_area(self):
        return 4 * math.pi * self.radius ** 2

    def diameter(self):
        return 2 * self.radius


class Triangle(Shape):
    title = "Triangle"

    def create(self, side_a, height):
        self.side_a = side_a
        self.height = height

    def area(self):
        return 1 / 2 * self.side_a * self.height

    def perimeter(self):
        return 3 * self.side_a


class Pyramid(Triangle):
    title = "Pyramid"

    def __init__(self):
        self.methods = ["Volume", "Surface Area"]

    def create(self, side_a, height):
        self.side_a = side_a
        self.height = height

    def volume(self):
        return 1 / 3 * self.side_a ** 2 * self.height

    def surface_area(self):
        return self.side_a ** 2 + 2*self.side_a*math.sqrt((self.side_a**2)/4 + self.height**2)


class Trapezoid(Shape):
    title = "Trapezoid"

    def __init__(self):
        self.methods = ["Area", "Perimeter"]

    def create(self, a, b, h):
        self.side_a = a
        self.side_b = b
        self.height = h

    def area(self):
        return 1 / 2 * self.height * (self.side_a * self.side_b)

    def perimeter(self):
        return self.side_a + self.side_b + 2 * math.sqrt(((abs(self.side_a - self.side_b)/2)
                                                          ** 2 + self.height**2))


class Rhombus(Shape):
    title = "Rhombus"

    def __init__(self):
        self.methods = ["Area", "Perimeter"]

    def create(self, d1, d2):
        self.d1 = d1
        self.d2 = d2

    def area(self):
        return 1 / 2 * self.d1 * self.d2

    def perimeter(self):
        return 2 * math.sqrt(self.d1 ** 2 + self.d2 ** 2)


class Cylinder(Shape):
    title = "Cylinder"

    def __init__(self):
        self.methods = ["Volume", "Surface Area"]

    def create(self, r, h):
        self.radius = r
        self.height = h

    def volume(self):
        return math.pi * self.radius ** 2 * self.height

    def surface_area(self):
        return 2 * math.pi * self.radius * (self.height + self.radius)


class Cone(Cylinder):
    title = "Cone"

    def volume(self):
        return 1 / 3 * self.height * math.pi * self.radius ** 2

    def surface_area(self):
        return math.pi * self.radius * (self.radius + math.sqrt(self.radius ** 2
                                                                + self.height ** 2))
