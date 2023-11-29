from turtle import Turtle, Screen
import random

screen = Screen()
screen.setup(width=500, height=400)

colors = ['red', 'green', 'blue', 'orange', 'purple', 'pink']
turtles = []
start_y = -150
for i in range(6):
    turtle = Turtle(shape="turtle")
    turtle.color(colors[i])
    turtle.penup()
    turtle.goto(x = -230, y = start_y + i*60)
    turtles.append(turtle)

is_race_on = False

user_bet = screen.textinput(title="Make Your Bet", prompt="Which turtle will win the race? Enter a color: ")

if user_bet:
    is_race_on = True

while is_race_on: 
    for turtle in turtles:
        rand_dist = random.randint(0,10)
        turtle.forward(rand_dist)
        if turtle.xcor() > 230:
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                print("You've won")
            else:
                print(f"You lost. {winning_color} turtle won.")
            is_race_on = False
            break

screen.exitonclick()
