import turtle
from random import randint, choice

turtle.shape('turtle')
turtle.forward(-300)
turtle.speed(10)
turtle.tracer(False)

def randomise():
    s = ["+", "−"]
    return f"F{choice(s)}[[X]{choice(s)}X]{choice(s)}F[{choice(s)}FX]{choice(s)}X"

# создаем грамматику
circuit = "FX"
rules = {"X": "F−[[X]+X]+F[+FX]−X",
         "F": "FF",
         "−": "−",
         "+": "+",
         "[": "[",
         "]": "]"}


class Stack:
    def __init__(self):
        self.s = []

    def append(self, x):
        self.s.append(x)

    def give(self):
        a = self.s.pop(-1)
        return a


def next_generation(c):
    c = list(c)
    for i in range(len(c)):
        if c[i] != "X":
            c[i] = rules[c[i]]
        else:
            c[i] = randomise()
    return str("".join(c))


n = 6
for i in range(n):
    circuit = next_generation(circuit)
    print(i)

q = Stack()


def forward():
    turtle.forward(3)


def right():
    turtle.right(randint(5, 30))


def left():
    turtle.left(randint(5, 30))

def save():
    x, y = turtle.pos()
    angle = turtle.heading()
    q.append((x, y, angle))

def restore():
    state = q.give()
    turtle.goto(state[0], state[1])
    turtle.setheading(state[2])


def nothing():
    pass


moves = {"F": forward,
         "+": right,
         "−": left,
         "[": save,
         "]": restore,
         "X": nothing}

for elem in circuit:
    moves[elem]()



turtle.exitonclick()
