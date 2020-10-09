import pygame
from pygame.draw import *
import numpy as np

pygame.init()

FPS = 30
screen = pygame.display.set_mode((600, 800))
# небо
rect(screen, (75, 75, 75), (0, 0, 600, 350))
# луна
circle(screen, (255, 255, 255), (500, 100), 70)
# облака (белогривые лошадки :)
ellipse(screen, (55, 55, 55), (200, 100, 300, 50))
ellipse(screen, (45, 45, 45), (350, 150, 250, 50))
ellipse(screen, (35, 35, 35), (50, 25, 500, 60))


def house(surf):
    # дом
    x, y, width, height = 50, 200, 300, 500
    rect(surf, (45, 35, 19), (x, y, width, height))
    # крыша
    polygon(surf, (20, 20, 20), ([x + 15, y - 25], [x + width - 15, y - 25], [x + 15 + width, y], [x - 15, y]))
    rect(surf, (45, 45, 45), (x + 30, y - 65, 15, 40))
    rect(surf, (45, 45, 45), (x + 60, y - 100, 30, 90))
    rect(surf, (35, 35, 35), (x + 250, y - 100, 15, 75))
    rect(surf, (45, 45, 45), (x + 160, y - 100, 20, 90))
    # окна
    for i in range(4):
        rect(surf, (222 - 50, 184 - 50, 135 - 50), (x + 25 + 70 * i, y, 40, 230))
    # балкон
    rect(surf, (25, 25, 25), (x - 25, y + 230, width + 50, 50))
    rect(surf, (25, 25, 25), (x - 25, y + 160, width + 50, 20))
    for i in range(7):
        rect(surf, (25, 25, 25), (x + 25 + i * 40, y + 180, 10, 50))
    # окна
    for i in range(3):
        if i == 2:
            rect(surf, (255, 255, 0), (x + 30 + i * 90, y + 300, 60, 100))
            break
        rect(surf, (55 + 30, 35 + 30, 19 + 30), (x + 30 + i * 90, y + 300, 60, 100))


# дома
for i in range(3):
    surface_h1 = pygame.Surface((600, 800))
    house(surface_h1)
    surface_h1 = pygame.transform.scale(surface_h1, (surface_h1.get_width() // 2, surface_h1.get_height() // 2))
    surface_h1.set_colorkey((0, 0, 0))
    screen.blit(surface_h1, (30 + 190 * i, 250 - 60 * i))

# облака
surface_c1 = pygame.Surface((600, 800))
surface_c1.set_alpha(60)
ellipse(surface_c1, (85, 85, 85), (400, 150 + 200, 250, 50))
ellipse(surface_c1, (85, 85, 85), (50, 210 + 200, 250, 50))
ellipse(surface_c1, (85, 85, 85), (250, 280 + 200, 250, 50))
surface_c1.set_colorkey((0, 0, 0))
screen.blit(surface_c1, (0, 0))


def ghost(surf, point=(500, 500)):
    circle(surf, (200, 200, 200), point, 50)
    # polygon(screen, (255, 255, 255), (
    # [point[0] - 50, point[1]], [point[0] - 100, point[1] + 200], [point[0] + 100, point[1] + 170],
    # [point[0] + 50, point[1]]))
    # решаем СЛАУ чтобы найти полином описывающий точки приведения и сделать красивые плавные границы
    from_x_to_xy = lambda x, coef: sum([coef[i] * x ** i for i in range(len(coef))])
    # кладем все точки приведения
    points = []

    ghost_side_left = [[450, 500], [440, 560], [430, 590], [420, 630], [410, 660], [400, 670], [390, 675], [380, 710]]
    coef_matrix = np.array([[1, elem[0], elem[0] ** 2, elem[0] ** 3, elem[0] ** 4, elem[0] ** 5, elem[0] ** 6,
                             elem[0] ** 7] for elem in ghost_side_left])
    vector = np.array(list(map(lambda x: x[1], ghost_side_left)))
    coef_polynom = np.linalg.solve(coef_matrix, vector)

    x = list(range(380, 451))
    left_points = [[elem, int(from_x_to_xy(elem, coef_polynom))] for elem in x]
    left_points.reverse()
    points.extend(left_points)

    x = np.arange(381, 601)
    y = list(15 * np.cos(x / 15) + 710 - 20 * np.cos(380 / 15))
    ghost_side_down = [[x[i], int(y[i])] for i in range(len(x))]
    points.extend(ghost_side_down)

    points.extend([[550, 500], [450, 500]])
    polygon(surf, (200, 200, 200), points)
    # рисуем глаза
    circle(surf, (100, 200, 250), (point[0] - 20, point[1] - 20), 10)
    circle(surf, (100, 200, 250), (point[0] + 20, point[1] - 20), 10)
    circle(surf, (0, 0, 0), (point[0] - 18, point[1] - 22), 6)
    circle(surf, (0, 0, 0), (point[0] + 22, point[1] - 22), 6)
    ellipse(surf, (255, 255, 255), [point[0] + 24, point[1] - 25, 3, 2])
    ellipse(surf, (255, 255, 255), [point[0] - 16, point[1] - 25, 3, 2])


def draw_ghost(surf, coord, scale, alpha, mirroring=False):
    ghost(surf)
    surf = pygame.transform.scale(surf, (int(surf.get_width() / scale), int(surf.get_height() / scale)))
    surf = pygame.transform.rotate(surf, 5)
    if mirroring:
        surf = pygame.transform.flip(surf, True, False)

    surf.set_alpha(alpha)
    screen.blit(surf, coord)


surf_g = pygame.Surface((600, 800))
surf_g.set_colorkey((0, 0, 0))
draw_ghost(surf_g, (290, 270), 2.5, 150)
draw_ghost(surf_g, (250, 290), 2.0, 160)
draw_ghost(surf_g, (0, 200), 1.3, 200)
draw_ghost(surf_g, (250, 400), 2.3, 130)
draw_ghost(surf_g, (0, 300), 2.5, 150, True)
draw_ghost(surf_g, (0, 350), 2.0, 160, True)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
