from turtle import Turtle, Screen
import random, time

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor('black')
screen.title('Snake Game')

class Snake:
    def __init__(self, length=3):
        self.turtles = []
        x = 0
        for _ in range(length):
            turtle = Turtle(shape='square')
            turtle.penup()
            turtle.color('white')
            turtle.goto(x = x, y = 0)
            x -= 20
            self.turtles.append(turtle)
        self.head = self.turtles[0]

    def extend(self):
        tail = Turtle(shape='square')
        tail.penup()
        tail.color('white')
        tail.goto(self.turtles[-1].position())
        self.turtles.append(tail)

    def intersect(self):
        for tt in self.turtles[1:]:
            if self.head.distance(tt) < 10:
                return True
        return False
    
    def move(self):
        for i in range(len(self.turtles)-1, 0, -1):
            tt = self.turtles[i]
            prev_tt = self.turtles[i-1]
            tt.goto(prev_tt.pos())
        self.head.forward(20)
    
    def up(self):
        if self.head.heading() != 270:
            self.head.setheading(90)
    
    def down(self):
        if self.head.heading() != 90:
            self.head.setheading(270)
    
    def left(self):
        if self.head.heading() != 0:
            self.head.setheading(180)
    
    def right(self):
        if self.head.heading() != 180:
            self.head.setheading(0)

class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color('blue')
        self.speed('fastest')
        self.refresh()

    def refresh(self):
        rand_x = random.randint(-250, 250)
        rand_y = random.randint(-250, 250)
        self.goto((rand_x, rand_y))

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.pencolor('white')
        self.penup()
        self.goto(0,280)
        self.write(f"Score: {self.score}", align='center', font=('Courier', 20, 'bold'))
        self.hideturtle()
    
    def increment_score(self):
        self.score += 1
        self.clear()
        self.write(f"Score: {self.score}", align='center', font=('Courier', 20, 'bold'))

    def game_over(self):
        self.goto(0,0)
        self.write("Game Over", align='center', font=('Courier', 20, 'bold'))


screen.tracer(0)
snake = Snake()
food = Food()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(snake.up, 'Up')
screen.onkey(snake.down, 'Down')
screen.onkey(snake.left, 'Left')
screen.onkey(snake.right, 'Right')


game_is_on = True
while game_is_on:
    time.sleep(0.2)
    snake.move()
    screen.update()

    if snake.head.distance(food) < 20:
        food.refresh()
        snake.extend()
        scoreboard.increment_score()
    
    if snake.head.xcor() >= 280 or snake.head.xcor() <= -280 \
        or snake.head.ycor() >= 280 or snake.head.ycor() <= -280 or \
        snake.intersect():
        game_is_on = False
        scoreboard.game_over()



screen.exitonclick()

# colors = ['red', 'green', 'blue', 'orange', 'purple', 'pink']
# turtles = []
# start_y = -150
# for i in range(6):
#     turtle = Turtle(shape="turtle")
#     turtle.color(colors[i])
#     turtle.penup()
#     turtle.goto(x = -230, y = start_y + i*60)
#     turtles.append(turtle)

# is_race_on = False

# user_bet = screen.textinput(title="Make Your Bet", prompt="Which turtle will win the race? Enter a color: ")

# if user_bet:
#     is_race_on = True

# while is_race_on: 
#     for turtle in turtles:
#         rand_dist = random.randint(0,10)
#         turtle.forward(rand_dist)
#         if turtle.xcor() > 230:
#             winning_color = turtle.pencolor()
#             if winning_color == user_bet:
#                 print("You've won")
#             else:
#                 print(f"You lost. {winning_color} turtle won.")
#             is_race_on = False
#             break


