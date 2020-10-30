import turtle

turtle.shape('turtle')
turtle.speed(10)
turtle.tracer(False)

# создаем грамматику
circuit = "FX"
rules = {"X": "X+YF+",
         "Y": "−FX−Y",
         "F": "F",
         "−": "−",
         "+": "+"}


def next_generation(c):
    c = list(c)
    for i in range(len(c)):
        c[i] = rules[c[i]]
    return str("".join(c))


n = 14
for i in range(n):
    circuit = next_generation(circuit)
    print(i)


def forward():
    turtle.forward(10)


def right():
    turtle.right(90)


def left():
    turtle.left(90)


def nothing():
    pass


moves = {"F": forward,
         "+": right,
         "−": left,
         "X": nothing,
         "Y": nothing}

for elem in circuit:
    moves[elem]()

turtle.exitonclick()
