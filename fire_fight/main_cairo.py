import sys
import pygame
import cairo

from fire_fight.hexgon import Hex, Layout, Point, layout_pointy, pixel_to_hex  # 根据你的文件命名适当导入
# 假设 hexgrid.py 内含有:
# Hex类(含corners方法, to_pixel方法), Layout类, Point类, layout_pointy等与之前一样的定义

pygame.init()
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hex Grid with Cairo")

hex_size = Point(30, 30)
origin = Point(WIDTH // 2, HEIGHT // 2)
layout = Layout(layout_pointy, hex_size, origin)

radius = 11
hexes_to_draw = []
for q in range(-radius, radius + 1):
    for r in range(-radius, radius + 1):
        s = -q - r
        h = Hex(q, r, s)
        if h.length() <= radius:
            hexes_to_draw.append(h)

clock = pygame.time.Clock()
running = True

def draw_hex_cairo(ctx, hex_obj: Hex, layout: Layout, fill_col=(0.86, 0.86, 0.86), line_col=(0,0,0), line_width=1, highlight=False):
    corners = hex_obj.corners(layout)
    # Cairo 使用浮点坐标，直接传入即可
    # corners: [Point(x, y), ...]
    # 移动到第一个点
    ctx.move_to(corners[0].x, corners[0].y)
    for p in corners[1:]:
        ctx.line_to(p.x, p.y)
    ctx.close_path()

    # 填充
    ctx.set_source_rgb(*fill_col)
    ctx.fill_preserve()

    # 画线条
    if highlight:
        # 假设高亮时加粗
        ctx.set_line_width(line_width+5)
    else:
        ctx.set_line_width(line_width)
    ctx.set_source_rgb(*line_col)
    ctx.stroke()

while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 将 Pygame 的 surface 转换为可供 cairo 使用的 surface
    # 这里使用的像素格式默认是32位 RGBA，与pygame.surfarray兼容。
    # 获取 Pygame Surface 的像素数据指针
    data = pygame.image.tostring(screen, "RGBA", True)
    # 创建与 pygame Surface 同大小的 cairo ImageSurface（基于内存数组）
    # 注意: cairo 要求一个可写字节数组作为 data source，这里我们要先创建一个 bytearray 再重写它
    surf_data = bytearray(data)
    cairo_surface = cairo.ImageSurface.create_for_data(
        surf_data,
        cairo.FORMAT_ARGB32,
        WIDTH,
        HEIGHT,
        WIDTH * 4
    )

    ctx = cairo.Context(cairo_surface)
    # 设置抗锯齿
    ctx.set_antialias(cairo.ANTIALIAS_BEST)

    # 填充背景为白色
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()

    # 获取鼠标位置并转换为 Hex 坐标
    mx, my = pygame.mouse.get_pos()
    hover_hex = pixel_to_hex(layout, Point(mx, my))

    # 绘制所有 hex
    for h in hexes_to_draw:
        highlight = (h == hover_hex)
        draw_hex_cairo(ctx, h, layout, fill_col=(0.86,0.86,0.86), line_col=(0,0,0), line_width=1, highlight=highlight)

    # 将 cairo 绘制结果更新回 Pygame surface
    # 将 cairo_surface 中的数据写回 pygame surface
    # 因为我们使用的 data = pygame.image.tostring(...) 是只读得到字符串，需要把修改写回pygame surface
    # 简单的方法是重新从 cairo surface 中读取图像字节再 blit 回 screen：
    out_data = cairo_surface.get_data()  # 这就是内存中的ARGB数据
    new_surf = pygame.image.frombuffer(out_data, (WIDTH, HEIGHT), "ARGB")
    screen.blit(new_surf, (0,0))

    pygame.display.flip()

pygame.quit()
sys.exit()

