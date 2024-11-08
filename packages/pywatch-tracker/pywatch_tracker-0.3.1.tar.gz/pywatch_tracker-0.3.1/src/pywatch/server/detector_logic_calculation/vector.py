import math
import typing
from dataclasses import dataclass

__all__ = ["euler_order", "Vector"]

euler_order = typing.Literal["xyz", "xzy", "yzx", "yxz", "zyx", "zxy"]


@dataclass
class Vector(list):
    Vector = typing.TypeVar("Vector")
    x: float = 0
    y: float = 0
    z: float = 0

    def __post_init__(self):
        super().__init__(self)
        super().extend([self.x, self.y, self.z])

    def norm(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def x_rotate(self, angle: float) -> Vector:
        angle *= math.pi / 180
        return Vector(
            self.x,
            self.y * math.cos(angle) - self.z * math.sin(angle),
            self.y * math.sin(angle) + self.z * math.cos(angle),
        )

    def y_rotate(self, angle: float) -> Vector:
        angle *= math.pi / 180
        return Vector(
            self.x * math.cos(angle) - self.z * math.sin(angle),
            self.y,
            self.x * math.sin(angle) + self.z * math.cos(angle),
        )

    def z_rotate(self, angle: float) -> Vector:
        angle *= math.pi / 180
        return Vector(
            self.x * math.cos(angle) - self.y * math.sin(angle),
            self.x * math.sin(angle) + self.y * math.cos(angle),
            self.z
        )

    def rotate_on_axis(self, axis: typing.Literal["x", "y", "z"], angle: float) -> Vector:
        if axis.lower() == "x":
            return self.x_rotate(angle)
        elif axis.lower() == "y":
            return self.y_rotate(angle)
        elif axis.lower() == "z":
            return self.z_rotate(angle)
        else:
            raise ValueError("axis has to be x, y or z.")

    def rotate(self, order: euler_order, angles: Vector) -> Vector:
        result = self

        for (i, axis), angle in zip(enumerate(order), [angles.x, angles.y, angles.z]):
            result = result.rotate_on_axis(axis, angle)  # type: ignore

        return result

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: typing.Union[Vector, float]) -> typing.Union[float, Vector]:
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y + self.z * other.z
        elif isinstance(other, (float, int)):
            return Vector(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError(f"operand '+' not supported for types Vector and {type(other)}")

    def __rmul__(self, other: float) -> Vector:
        return self.__mul__(other)

    def __truediv__(self, other: float) -> Vector:
        return self * (1 / other)

    def __str__(self) -> str:
        return f"({round(self.x, 10)}, {round(self.y, 10)}, {round(self.z, 10)})"

    def __repr__(self) -> str:
        return self.__str__()
