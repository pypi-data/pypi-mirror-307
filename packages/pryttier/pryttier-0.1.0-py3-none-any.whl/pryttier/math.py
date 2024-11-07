from typing import *
from numpy import *
from .graphing import *

PI = 2 * acos(0)
Degrees = PI / 180


def summation(n: float | int, i: float | int, expr: Callable) -> float:
    total = 0
    for j in range(n, i + 1):
        total += expr(j)
    return total


def product(n: int, i: int, expr: Callable) -> float:
    total = 1
    for j in range(n, i):
        total *= expr(j)
    return total


def clamp(num: float, low: float, high: float) -> float:
    if (num > low) and (num < high):
        return num
    else:
        if num < low:
            return low
        if num > high:
            return high


def sign(num: float) -> int:
    return int(num / abs(num))


def factorial(num: int) -> int:
    if num == 0:
        return 1
    if num == 1:
        return 1
    return num * factorial(num - 1)


def binToDec(num: int) -> int:
    digits = [int(i) for i in list(str(num))]
    total = 0
    for j in range(0, len(digits)):
        total += (2 ** j) * (digits[j])
    return total


def mapRange(value: int | float,
             min1: float,
             max1: float,
             min2: float,
             max2: float) -> float:
    return (value - min1) / (max1 - min1) * (max2 - min2) + min2


class Vector2:
    def __init__(self,
                 x: float | int,
                 y: float | int):
        self.x = x
        self.y = y
        self.length = sqrt(self.x * self.x + self.y * self.y)

    def __str__(self) -> str:
        return f"{self.x}i + {self.y}j"

    def __add__(self, other: Self) -> Self:
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, other: Self | float | int) -> Self:
        if isinstance(other, float) or isinstance(other, int):
            return Vector2(self.x * other, self.y * other)
        elif isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)

    def __sub__(self, other: Self) -> Self:
        return Vector2(self.x - other.x, self.y - other.y)

    def normalize(self) -> Self:
        return Vector2(self.x / self.length, self.y / self.length)

    def __truediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector2(self.x / other, self.y / other)
        elif isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)


class Vector3:
    def __init__(self,
                 x: float | int,
                 y: float | int,
                 z: float | int):
        self.x = x
        self.y = y
        self.z = z
        self.length = sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __repr__(self) -> str:
        return f"{self.x}i + {self.y}j + {self.z}k"

    def __add__(self, other: Self) -> Self:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Self) -> Self:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Self | float | int) -> Self:
        if isinstance(other, float) or isinstance(other, int):
            return Vector3(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

    def normalize(self) -> Self:
        return Vector3(self.x / self.length, self.y / self.length, self.z / self.length)

    def __truediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector3(self.x / other, self.y / other, self.z / other)
        elif isinstance(other, Vector3):
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)


def cross(a: Vector2 | Vector3,
          b: Vector2 | Vector3) -> Vector3 | float:
    raise NotImplemented("Sorry, but this function is planned for a future update")


def distance(a: Vector2 | Vector3,
             b: Vector2 | Vector3):
    if (isinstance(a, Vector2)) and (isinstance(b, Vector2)):
        return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)
    elif isinstance(a, Vector3) and isinstance(b, Vector3):
        return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2 + (b.z - a.z) ** 2)
    else:
        raise TypeError("Error in Calculation")


def linearInterpolation2D(p1: Vector2, p2: Vector2, step: int):
    interpolation = []

    interpolation.append(p1)
    interpolation.append(p2)

    for i in range(p1.x, p2.x, step):
        x = i / 255
        m = (p2.y - p1.y) / (p2.x - p1.x)
        y = p1.y + (x - p1.x) * m
        interpolation.append(Vector2(x, y))

    return interpolation
