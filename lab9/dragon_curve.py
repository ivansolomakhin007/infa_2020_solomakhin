import turtle

turtle.shape('turtle')
turtle.speed(10)
turtle.tracer(False)

# создаем грамматику
circuit = "FX"
rules = {"X": "X+YF+",
         "Y": "−FX−Y"}
def next_generation(c):
    c = list(c)
    for i in range(len(c)):
        if c[i] == "X":
            c[i] = "X+YF+"
        elif c[i] == "Y":
            c[i] = "−FX−Y"
    return str("".join(c))


for i in range(14):
    circuit = next_generation(circuit)

for elem in circuit:
    if elem == "F":
        turtle.forward(10)
    elif elem == "+":
        turtle.right(90)
    elif elem == "−":
        turtle.left(90)

turtle.exitonclick()
