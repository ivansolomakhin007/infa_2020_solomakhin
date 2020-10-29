from random import randrange as rnd, choice
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class ball():
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 30

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        # self.vy += 1
        self.x += self.vx
        self.y -= self.vy
        self.vy -= 1
        self.set_coords()
        if self.x >= 800 or self.x <= 0:
            self.vx *= -1
        if self.y >= 600 or self.y <= 0:
            self.vy *= -1

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        return (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20, 450, 50, 420, width=7)  # FIXME: don't know how to set it...

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        ###
        if balls:
            canv.delete(balls[0].id)
            balls.clear()
        ###
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class target():
    def __init__(self):
        self.points = 0
        self.live = 1
        self.targets = []

        # FIXME: don't work!!! How to call this functions when object is created?
        # def a(self):
        # self.id = canv.create_oval(0, 0, 0, 0)
        #self.id_points = canv.create_text(30, 30, text=self.points, font='28')
        # self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        self.id = canv.create_oval(0, 0, 0, 0)

        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points
        ###
        #self.id_points = canv.create_text(30, 30, text=self.points, font='28')
        ###
        # canv.itemconfig(self.id_points, text=self.points)

    def move(self):
        self.v_x = rnd(-10, +10)
        self.v_y = ((-1)**(choice([1, 2]))) * (100 - self.v_x ** 2)**0.5
        self.x += self.v_x
        self.y += self.v_y
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r)


t1 = target()
t2 = target()
screen1 = canv.create_text(400, 300, text='', font='28')
screen2 = canv.create_text(0, 0, text='', font='28')

# g1 = gun()
bullet = 0
balls = []
flag = True

#screen2 = canv.create_text(30, 30, text='', font='28')


def new_game(event=''):
    global gun, t1, screen1, screen2, balls, bullet
    # t1 = target()
    canv.itemconfig(screen1, text='')
    canv.itemconfig(screen2, text='')


    # t1.new_target()
    # t2.new_target()
    t1.new_target()
    t2.new_target()
    ###
    g1 = gun()
    bullet = 0
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    screen1 = canv.create_text(400, 300, text='', font='28')

    screen2 = canv.create_text(30, 30, text='', font='28')

    canv.itemconfig(screen2, text=(t1.points + t2.points))

    z = 0.03
    t1.live = 1
    t2.live = 1
    while t1.live or t2.live or balls:

        for b in balls:
            b.move()
            if b.hittest(t1) and t1.live:
                t1.live = 0
                t1.hit()
                canv.delete(balls[0].id)
                balls.clear()
                canv.delete(t1.id)
                # canv.delete(balls[0].id)
                #canv.bind('<Button-1>', '')
                #canv.bind('<ButtonRelease-1>', '')
                print("мы сейчас в ифе")
                #canv.itemconfig(screen1,
                                #text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов\nДля рестарта нажмити Enter')
            if b.hittest(t2) and t2.live:
                t2.live = 0
                t2.hit()
                canv.delete(balls[0].id)
                balls.clear()
                canv.delete(t2.id)
                # canv.delete(balls[0].id)
                #canv.bind('<Button-1>', '')
                #canv.bind('<ButtonRelease-1>', '')
                # canv.itemconfig(screen1,
                # text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов\nДля рестарта нажмити Enter')
            canv.itemconfig(screen2, text=(t1.points + t2.points))
            t1.move()
            t2.move()

        if t1.live == 0 and t2.live == 0:
            canv.delete(g1.id)
            balls.clear()
            canv.bind('<Button-1>', '')
            canv.bind('<ButtonRelease-1>', '')
            print("aaaaaaaaaaaaaaaaaaa")
            canv.itemconfig(screen1,
                            text='Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
            ###
            #canv.delete("all")


        canv.update()
        time.sleep(z)
        g1.targetting()
        g1.power_up()

    #canv.itemconfig(screen1, text='')
    canv.delete(gun)

    root.after(750, new_game)
    #canv.itemconfig(screen1, text='')



new_game()
root.mainloop()
