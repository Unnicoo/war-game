from enum import Enum, auto

from fire_fight.hexgon import Hex
from pygame import Color


class TileType(Enum):
    # cell itself
    OPEN_GROUND = 0
    FOREST = 1
    TOWN = 2
    RIVER = 3
    # maybe edge
    ROAD = 4
    PATH = 5
    REVERSE_SLOPE = 6
    CONTOUR_LINE = 7
    BRIDGE = 8
    SMOKE_SCREEN = 9
    PERSONNEL_SHELTER = 10


# Mapping Enum to colors
TILE_COLOR_MAP = {
    TileType.OPEN_GROUND: Color(200, 200, 200),
    TileType.FOREST: Color(34, 139, 34),
    TileType.TOWN: Color(139, 69, 19),
    TileType.RIVER: Color(0, 191, 255),
    TileType.ROAD: Color(128, 128, 128),
    TileType.PATH: Color(160, 82, 45),
    TileType.REVERSE_SLOPE: Color(205, 133, 63),
    TileType.CONTOUR_LINE: Color(255, 215, 0),
    TileType.BRIDGE: Color(139, 0, 0),
    TileType.SMOKE_SCREEN: Color(192, 192, 192),
    TileType.PERSONNEL_SHELTER: Color(128, 0, 128),
}


class HexTile:
    def __init__(self, q: int, r: int, s: int, tile_type: TileType) -> None:
        self.hex = Hex(q, r, s)
        self.tile_type = tile_type
