from turtle import Turtle, Screen
from random import random, choice

my_turtle = Turtle()
my_turtle.shape('turtle')
my_turtle.color('purple')

# my_turtle.forward(100)
# my_turtle.right(90)
# my_turtle.forward(100)
# my_turtle.right(90)
# my_turtle.forward(100)
# my_turtle.right(90)
# my_turtle.forward(100)
# my_turtle.right(90)

# my_turtle.penup()
# my_turtle.setpos(-600,0)
# for i in range(50):
#     my_turtle.pendown()
#     my_turtle.forward(10)
#     my_turtle.penup()
#     my_turtle.forward(10)

# for i in range(3,11):
#     my_turtle.color(random(), random(), random())
#     turn_angle = 360 / i
#     for j in range(i):
#         my_turtle.forward(100)
#         my_turtle.right(turn_angle)


# steps = 5000
# angles = [0, 90, 180, 270]
# my_turtle.pensize(4)
# my_turtle.speed('fastest')

# for i in range(steps):
#     my_turtle.color(random(), random(), random())
#     my_turtle.left(choice(angles))
#     my_turtle.forward(10)

for i in range(0, 360, 5):
    my_turtle.setheading(i)
    my_turtle.color(random(), random(), random())
    my_turtle.circle(100)

screen = Screen()
screen.screensize(4000,3000)
screen.exitonclick()