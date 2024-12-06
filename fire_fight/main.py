import sys
import pygame
import pygame.gfxdraw
from pygame import Color
from fire_fight.hexgon import Hex, Layout, Point, layout_pointy, layout_flat, pixel_to_hex

# 初始化 pygame
pygame.init()

# 设置窗口大小与标题
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hex Grid Example")

# 定义布局 (根据你的布局选择，下面以pointy-top为例)
# 假设每个六边形的边长为 30 像素
hex_size = Point(45, 45)
origin = Point(WIDTH//2, HEIGHT//2)  # 可以将原点放在屏幕中心
layout = Layout(layout_pointy, hex_size, origin)

# 定义要绘制的范围（q,r坐标范围）
# 假设绘制一个中心在 (0,0,-0) 附近的区域
radius = 11  # 绘制半径为 5 的六边形（即从中心往各方向5步）
hexes_to_draw = []
for q in range(-radius, radius+1):
    for r in range(-radius, radius+1):
        s = -q - r
        # 只绘制在 radius 范围内的六边形（使用 hex distance 确定）
        hex_coord = Hex(q, r, s)
        if hex_coord.length() <= radius:
            hexes_to_draw.append(hex_coord)

# 定义一个函数来绘制一个 hex 的轮廓
def draw_hex_outline(surface, hex_obj: Hex, layout: Layout, color=Color("black"), width=1):
    corners = hex_obj.corners(layout)
    # corners 是 [Point(x1, y1), Point(x2, y2), ..., Point(x6, y6)]
    # 将其转换为 pygame 可绘制的点列表
    points = [(p.x, p.y) for p in corners]
    # 使用 draw.polygon 绘制一个多边形的线框
    pygame.draw.polygon(surface, color, points, width)
    pygame.gfxdraw.aapolygon(surface, points, color)    # 抗锯齿轮廓

# 定义一个函数来填充一个 hex
def fill_hex(surface, hex_obj: Hex, layout: Layout, color=Color("white")):
    corners = hex_obj.corners(layout)
    points = [(p.x, p.y) for p in corners]
    pygame.draw.polygon(surface, color, points, 0)
    # pygame.gfxdraw.filled_polygon(surface, points, color) # 填充（可选）

# 游戏主循环
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(30)  # 控制帧率为30FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充背景
    screen.fill((255, 255, 255))

    # 获取鼠标位置并转换为 Hex 坐标
    mx, my = pygame.mouse.get_pos()
    hover_hex = pixel_to_hex(layout, Point(mx, my))

    for h in hexes_to_draw:
        # 填充颜色
        fill_hex(screen, h, layout, Color(220,220,220))

        # 如果该 hex 是鼠标悬浮的 hex，则边缘加粗
        draw_hex_outline(screen, h, layout, Color("black"), width=1)
    if hover_hex in hexes_to_draw:
        draw_hex_outline(screen, hover_hex, layout, Color("black"), width=4)

    # 刷新画面
    pygame.display.flip()

# 退出
pygame.quit()
sys.exit()
