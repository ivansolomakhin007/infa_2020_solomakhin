import turtle

turtle.shape('turtle')
turtle.speed(10)
turtle.tracer(False)

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
        c[i] = rules[c[i]]
    return str("".join(c))


n = 6
for i in range(n):
    circuit = next_generation(circuit)
    print(i)

q = Stack()


def forward():
    turtle.forward(3)


def right():
    turtle.right(25)


def left():
    turtle.left(25)

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
