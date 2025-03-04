import sys
import json
import pygame
import random
import pygame.gfxdraw

from pygame import Color

from fire_fight.hexgon import (
    Hex,
    Layout,
    Point,
    layout_flat,
    layout_pointy,
    pixel_to_hex,
)
from fire_fight.tile import TILE_COLOR_MAP, HexTile, TileType


def fill_hex(surface, hex_obj: Hex, layout: Layout, color=Color("white")):
    corners = hex_obj.corners(layout)
    points = [(p.x, p.y) for p in corners]
    pygame.draw.polygon(surface, color, points, 0)
    # pygame.gfxdraw.filled_polygon(surface, points, color) # 填充（可选）


def draw_hex_outline(
    surface, hex_obj: Hex, layout: Layout, color=Color("black"), width=1
):
    corners = hex_obj.corners(layout)
    # corners 是 [Point(x1, y1), Point(x2, y2), ..., Point(x6, y6)]
    # 将其转换为 pygame 可绘制的点列表
    points = [(p.x, p.y) for p in corners]
    # 使用 draw.polygon 绘制一个多边形的线框
    pygame.draw.polygon(surface, color, points, width)
    pygame.gfxdraw.aapolygon(surface, points, color)  # 抗锯齿轮廓


def hex_to_pixel(layout: Layout, hex: Hex) -> Point:
    M = layout.orientation
    x = (M.f0 * hex.q + M.f1 * hex.r) * layout.size.x
    y = (M.f2 * hex.q + M.f3 * hex.r) * layout.size.y
    return Point(x + layout.origin.x, y + layout.origin.y)


# 初始化 pygame
pygame.init()

# 设置窗口
WIDTH, HEIGHT = 1200, 900
# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
# 设置标题
pygame.display.set_caption("Hex Grid Example")
# 设置字体
font = pygame.font.SysFont(None, 24)

# 定义布局 (根据你的布局选择，下面以pointy-top为例)
# 假设每个六边形的边长为 30 像素
hex_size = Point(30, 30)
origin = Point(WIDTH // 2, HEIGHT // 2)  # 可以将原点放在屏幕中心
layout = Layout(layout_pointy, hex_size, origin)

# read basic.json
file_path = r'C:/users/xxjw/desktop/hujiaozhua/map1.json'
with open(file_path, 'r') as f:
    basic = json.load(f)

# print(basic)

# get map size
basic_map = basic['map_data']
map_height = len(basic_map)
if map_height == 0:
    print("地图数据为空")
    sys.exit()

Cond = []
for r in range(len(basic_map)):
    map_width = len(basic_map[0]) - 1
    if len(basic_map[r]) - 1 != map_width:
        print(f'地图第{r+1}行宽度不一致,需要修改数据')
        sys.exit()
    for c in range(len(basic_map[r])):
        cond_num = basic_map[r][c]['cond']
        cond = TileType(cond_num)
        Cond.append(cond)

# Define hex grid dimensions (rectangle shape)
hexes_to_draw = []
all_hexes = []
count = 0
for r in range(-map_height // 2, map_height // 2):
    r_offset = (r + 1) // 2  # Offset for rectangular shape
    for q in range(-map_width // 2 - r_offset, map_width // 2 - r_offset + 1):      # noqa
        s = -q - r
        # hex_coord = Hex(q, r, s)
        row = count // (map_width + 1)
        col = count % (map_width + 1)
        cond = basic_map[row][col]['cond']
        tile_type = TileType(cond)
        hex_tile = HexTile(q, r, s, tile_type)
        hexes_to_draw.append(hex_tile)
        all_hexes.append(hex_tile.hex)
        count += 1


# Variables for panning
dragging = False
scale_factor = 1.0
last_mouse_pos = None

# 游戏主循环
running = True
# 创建一个帮助跟踪时间的对象，用于控制帧率
clock = pygame.time.Clock()

while running:
    # 设定最大帧率，限制主循环的执行速度
    clock.tick(120)

    # 从队列中获取事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                dragging = True
                last_mouse_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx, dy = mouse_x - last_mouse_pos[0], mouse_y - last_mouse_pos[1]
                layout.origin = Point(layout.origin.x + dx, layout.origin.y + dy)
                last_mouse_pos = (mouse_x, mouse_y)

    # 填充背景
    screen.fill((255, 255, 255))

    # 获取鼠标位置并转换为 Hex 坐标
    mx, my = pygame.mouse.get_pos()
    hover_hex = pixel_to_hex(layout, Point(mx, my))

    for idx, h in enumerate(hexes_to_draw):
        # 填充颜色
        fill_hex(screen, h.hex, layout, color=TILE_COLOR_MAP[h.tile_type])
        # 绘制其序号
        # 计算 Hex 的中心点
        center = h.hex.to_pixel(layout)
        # 创建要绘制的文本图像
        row = str(idx // (map_width + 1)).zfill(2)
        col = str(idx % (map_width + 1)).zfill(2)
        text_surface = font.render(f"{row}{col}", True, Color("black"))
        # 获取文本图像的尺寸
        text_rect = text_surface.get_rect(center=(center.x, center.y))
        # 在屏幕上绘制文本
        screen.blit(text_surface, text_rect)
        draw_hex_outline(screen, h.hex, layout, Color("black"), width=1)
    # draw this outline in the end, otherwise the line will be obscured by other draw function
    #
    if hover_hex in all_hexes:
        for i in range(6):
            hex = hover_hex.get_neighbor(i)
            if hex in all_hexes:
                draw_hex_outline(screen, hex, layout, Color("blue"), width=4)
        draw_hex_outline(screen, hover_hex, layout, Color("black"), width=4)

    # 刷新画面
    pygame.display.flip()

# 退出
pygame.quit()
sys.exit()
