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


# username = input("Введите username: ")


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
    sheet = load_image("sprite sheet.png")

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = randint(100, 1050)
        self.y = randint(-200, -100)
        self.v_x = randint(-30, 30)
        self.v_y = 20
        self.frames = []
        self.cut_sheet(self.sheet, 8, 8)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = self.x
        self.rect.y = self.y
        self.frame_count = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)

        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def click(self, mouse_pos):
        global count
        if self.rect.collidepoint(mouse_pos) and self.mask.get_at(
                (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)):
            self.kill()
            count += 2

    def update(self):
        if self.frame_count % 2 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.frame_count += 1
        self.image = self.frames[self.cur_frame]

        self.rect.x += self.v_x
        self.rect.y += self.v_y
        # self.v_y += 1

        if self.rect.y >= HEIGHT or self.rect.x >= WIDTH or self.rect.x <= 0:
            self.rect.y = HEIGHT - self.rect.y
            self.rect.x = WIDTH - self.rect.x
        # if abs(self.rect.x) >= WIDTH:
        #     self.rect.x = - self.rect.x


all_sprites = pygame.sprite.Group()
meteors = pygame.sprite.Group()

pygame.display.update()
clock = pygame.time.Clock()
finished = False
# подсчет о4ков
count = 0

# считаем игровое время
#start_ticks = pygame.time.get_ticks()
PLAYTIME = 15

# немного веселья
frames_count = 0
backgrounds = [(189, 0, 0), (44, 156, 19), (8, 124, 163), (201, 10, 198)]


def music(name):
    pygame.mixer.music.load(name)
    pygame.mixer.music.play()


music("song.mp3")

flag = False

MAX_BALLS = 5
MAX_METEORS = 3

def main_loop():
    """Главный цикл"""
    global finished, count
    start_ticks = pygame.time.get_ticks()
    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # проверяем попадание по спрайту
                for elem in all_sprites:
                    elem.click(event.pos)
                for elem in meteors:
                    elem.click(event.pos)
            if event.type == pygame.KEYDOWN:
                print(event.unicode)
        # контролируем количество шариков
        if len(all_sprites) < MAX_BALLS:
            all_sprites.add(Ball())
        all_sprites.update()
        all_sprites.draw(screen)
        if len(meteors) < MAX_METEORS:
            meteors.add(Meteor())
        meteors.update()
        meteors.draw(screen)
        # отрисовываем текст
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 50)
        textsurface = myfont.render(f'Счет: {count}', False, (255, 255, 255))
        screen.blit(textsurface, (0, 0))
        pygame.display.update()
        # меняем фон
        # if frames_count % 4 == 0:
        #     color = choice(backgrounds)
        # frames_count += 1
        screen.fill(BLACK)

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if seconds > PLAYTIME:
            user()
            count = 0
            break

#main_loop()


# вводим имя пользователя
def user():
    global finished
    us = []
    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    # если нажали на enter то полагаем, что имя пользователя введено и сохраняем рехультат
                    save(us)
                    return
                us.append(event.unicode)

        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 50)
        textsurface1 = myfont.render(f'{"".join(us)}', False, (255, 255, 255))
        screen.blit(textsurface1, (600, 300))
        textsurface2 = myfont.render("Введите имя пользователя и нажмите Enter", False, (255, 255, 255))
        screen.blit(textsurface2, (200, 200))
        pygame.display.update()
        screen.fill(BLACK)


#u = user()

def save(userrr):
    if not finished:
        with open("records.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        with open("records.txt", "w", encoding="utf-8") as f:
            lines.append(f"{''.join(userrr)} {count}")
            lines = list(map(str.strip, lines))
            lines = list(filter(lambda x: x, lines))
            lines = list(sorted(lines, key=lambda x: int(x.split()[1]), reverse=True))
            print(lines)
            if len(lines) > 10:
                lines = lines[:10]
            for line in lines:
                if line.strip():
                    f.write(line + "\n")

def main_menu():
    global finished
    while not finished:
        clock.tick(FPS)
        pos = (0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
        rect(screen, (0, 0, 0), (400, 250, 400, 50))
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 50)
        textsurface = myfont.render('Играть', False, (255, 255, 255))
        screen.blit(textsurface, (400, 250))
        #rect(screen, (0, 0, 0), (400, 250, 400, 50))
        if 400 <= pos[0] <= 800 and 250 <= pos[1] <= 300:
            main_loop()
        pygame.display.update()
        # меняем фон
        # if frames_count % 4 == 0:
        #     color = choice(backgrounds)
        # frames_count += 1
        screen.fill(BLACK)

main_menu()

pygame.quit()
