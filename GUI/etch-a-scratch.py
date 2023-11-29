from turtle import Turtle, Screen
import math

my_turtle = Turtle()

screen = Screen()
# screen.screensize(4000,3000)

def forward():
    my_turtle.forward(10)

def backward():
    my_turtle.backward(10)

def counter_clockwise():
    my_turtle.left(10)

def clockwise():
    my_turtle.right(10)

def clearscreen():
    my_turtle.penup()
    my_turtle.home()
    my_turtle.pendown()
    my_turtle.clear()


screen.onkeypress(forward, 'w')
screen.onkeypress(backward, 's')
screen.onkeypress(counter_clockwise, 'a')
screen.onkeypress(clockwise, 'd')
screen.onkeypress(clearscreen, 'c')
screen.listen()

screen.exitonclick()

