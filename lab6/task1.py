import pygame
from pygame.draw import *
from random import randint, choice

pygame.init()

FPS = 30
WIDTH = 1200
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

username = input("Введите username: ")


def load_image(name):
    return pygame.image.load(name)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        '''рисует новый шарик '''
        self.x = randint(100, 1050)
        self.y = randint(100, 400)
        self.r = randint(10, 100)
        self.v_x = randint(1, 20)
        self.v_y = int(choice([1, -1]) * (20 ** 2 - self.v_x ** 2) ** 0.5)

        self.color = COLORS[randint(1, 5)]
        self.image = pygame.Surface((2 * self.r, 2 * self.r))
        self.image.fill((0, 0, 0))
        circle(self.image, self.color, (self.r, self.r), self.r)
        self.image.set_colorkey((0, 0, 0))
        # создаем маску для кружка
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def click(self, mouse_pos):
        global count
        if self.rect.collidepoint(mouse_pos) and self.mask.get_at(
                (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)):
            self.kill()
            count += 1

    def update(self):
        self.rect.x += self.v_x
        self.rect.y += self.v_y
        if (self.rect.x + self.r * 2) >= WIDTH or self.rect.x <= 0:
            self.v_x *= -1

        if (self.rect.y + self.r * 2) >= HEIGHT or self.rect.y <= 0:
            self.v_y *= -1


class Meteor(pygame.sprite.Sprite):
    """класс метеора, летит сверху, в поле тяжести. а него даем два очка"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = randint(100, 1050)
        self.y = randint(-200, -100)
        self.v_x = randint(1, 5)
        self.v_y = 20
        self.image = pygame.image.load("meteor.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 4, self.image.get_height() // 4))
        # color = self.image.get_at((10, 10))
        # self.image.set_colorkey(color)
        self.image = self.image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

    def click(self, mouse_pos):
        global count
        if self.rect.collidepoint(mouse_pos) and self.mask.get_at(
                (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)):
            self.kill()
            count += 2

    def update(self):
        self.rect.x += self.v_x
        self.rect.y += self.v_y
        self.v_y += 0.5

        if self.rect.y >= HEIGHT:
            self.kill()


all_sprites = pygame.sprite.Group()
meteors = pygame.sprite.Group()

pygame.display.update()
clock = pygame.time.Clock()
finished = False
# подсчет о4ков
count = 0

start_ticks = pygame.time.get_ticks()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for elem in all_sprites:
                elem.click(event.pos)
            for elem in meteors:
                elem.click(event.pos)
    if len(all_sprites) < 5:
        all_sprites.add(Ball())
    all_sprites.update()
    all_sprites.draw(screen)
    if len(meteors) < 3:
        meteors.add(Meteor())
    meteors.update()
    meteors.draw(screen)
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 50)
    textsurface = myfont.render(f'Ващ счет: {count}', False, (255, 255, 255))
    screen.blit(textsurface, (0, 0))
    pygame.display.update()
    screen.fill(BLACK)
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    if seconds > 10:
        break
with open("records.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("records.txt", "w", encoding="utf-8") as f:
    lines.append(f"{username} {count}")
    lines.sort()
    for line in lines:
        if line:
            f.write(line)

pygame.quit()
