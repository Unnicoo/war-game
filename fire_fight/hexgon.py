from __future__ import annotations
import math
from dataclasses import dataclass, field

HEX_DIRECTION = [
    (1, 0, -1),
    (1, -1, 0),
    (0, -1, 1),
    (-1, 0, 1),
    (-1, 1, 0),
    (0, 1, -1),
]


def hex_round(q: float, r: float, s: float):
    qi = int(round(q))
    ri = int(round(r))
    si = int(round(s))
    q_diff = abs(qi - q)
    r_diff = abs(ri - r)
    s_diff = abs(si - s)
    if q_diff > r_diff and q_diff > s_diff:
        qi = -ri - si
    else:
        if r_diff > s_diff:
            ri = -qi - si
        else:
            si = -qi - ri
    return Hex(qi, ri, si)


def hex_corner_offset(layout: Layout, corner: int):
    size = layout.size
    angle = 2.0 * math.pi * (layout.orientation.start_angle + corner) / 6
    return Point(size.x * math.cos(angle), size.y * math.sin(angle))


@dataclass(frozen=True)
class Point:
    x: float | int
    y: float | int


HEX_CACHE = {}


@dataclass(frozen=True)
class Hex:
    q: int
    r: int
    s: int

    def __post_init__(self) -> None:
        assert self.q + self.r + self.s == 0, "q + r + s should equal 0"

    def __new__(cls, q: int, r: int, s: int):
        # 在 __new__ 中拦截实例创建
        key = (q, r, s)
        if key in HEX_CACHE:
            return HEX_CACHE[key]
        # 调用父类 __new__ 创建新实例
        obj = super().__new__(cls)
        # 使用object.__setattr__给冻结类赋值
        object.__setattr__(obj, "q", q)
        object.__setattr__(obj, "r", r)
        object.__setattr__(obj, "s", s)
        HEX_CACHE[key] = obj
        return obj

    def __add__(self, other: Hex) -> Hex:
        return Hex(self.q + other.q, self.r + other.r, self.s + other.r)

    def __sub__(self, other: Hex) -> Hex:
        return Hex(self.q - other.q, self.r - other.r, self.s - other.r)

    def __mul__(self, factor: int | float) -> Hex:
        assert isinstance(factor, int), "multiplier must be number"
        return Hex(self.q * factor, self.r * factor, self.s * factor)

    def length(self) -> int:
        return int((abs(self.q) + abs(self.r) + abs(self.s)) / 2)

    def dist_to(self, other: Hex) -> int:
        return (other - self).length()

    def to_pixel(self, layout: Layout) -> Point:
        M = layout.orientation
        x = (M.f0 * self.q + M.f1 * self.r) * layout.size.x
        y = (M.f2 * self.q + M.f3 * self.r) * layout.size.y
        return Point(x + layout.origin.x, y + layout.origin.y)

    def get_neighbor(self, direction: int) -> Hex:
        assert 0 <= direction < 6, "direction must be in range 0-5"
        if not (0 <= direction < 6):
            direction = (direction + 6) % 6
        return self + Hex(*HEX_DIRECTION[direction % 6])

    def corners(self, layout: Layout) -> list[Point]:
        center = self.to_pixel(layout)
        return [Point(center.x + o.x, center.y + o.y) for o in layout.corner_offsets]


@dataclass(frozen=True)
class Orientation:
    f0: float
    f1: float
    f2: float
    f3: float
    b0: float
    b1: float
    b2: float
    b3: float
    start_angle: float


@dataclass(frozen=True)
class Layout:
    orientation: Orientation
    size: Point
    origin: Point
    corner_offsets: list[Point] = field(default_factory=list, init=False)

    def __post_init__(self):
        offsets = [hex_corner_offset(self, i) for i in range(6)]
        object.__setattr__(self, "corner_offsets", offsets)


layout_pointy = Orientation(
    math.sqrt(3.0),
    math.sqrt(3.0) / 2.0,
    0.0,
    3.0 / 2.0,
    math.sqrt(3.0) / 3.0,
    -1.0 / 3.0,
    0.0,
    2.0 / 3.0,
    0.5,
)
layout_flat = Orientation(
    3.0 / 2.0,
    0.0,
    math.sqrt(3.0) / 2.0,
    math.sqrt(3.0),
    2.0 / 3.0,
    0.0,
    -1.0 / 3.0,
    math.sqrt(3.0) / 3.0,
    0.0,
)


def pixel_to_hex(layout: Layout, p: Point):
    M = layout.orientation
    pt = Point(
        (p.x - layout.origin.x) / layout.size.x,
        (p.y - layout.origin.y) / layout.size.y,
    )
    q = M.b0 * pt.x + M.b1 * pt.y
    r = M.b2 * pt.x + M.b3 * pt.y
    return hex_round(q, r, -q - r)
