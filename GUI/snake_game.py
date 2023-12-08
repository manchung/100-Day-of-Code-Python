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

    def reset(self):
        for turtle in self.turtles:
            turtle.goto(1000,1000)
            turtle.hideturtle()
        self.__init__()
    
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
        self.read_high_score_from_file()
        self.pencolor('white')
        self.penup()
        self.hideturtle()
        self.write_score()
    
    def write_score(self):
        self.clear()
        self.goto(0,280)
        self.write(f"Score: {self.score}  High Score: {self.high_score}", align='center', font=('Courier', 20, 'bold'))

    def increment_score(self):
        self.score += 1
        self.write_score()

    def game_over(self):
        self.goto(0,0)
        self.write("Game Over.", align='center', font=('Courier', 20, 'bold'))
        self.goto(0, -20)
        self.write("Type r to Restart, q to Quit", align='center', font=('Courier', 10, 'normal'))

    def reset(self):
        self.clear()
        if self.score > self.high_score:
            self.high_score = self.score 
        self.write_high_score_to_file()
        self.score = 0
        self.write_score()
    
    def write_high_score_to_file(self, filename='snake_high_score.txt'):
        with open(filename, 'w') as file:
            file.write(f"{self.high_score}")
    
    def read_high_score_from_file(self, filename='snake_high_score.txt'):
        try :
            with open(filename, 'r') as file:
                contents = file.read()
                self.high_score = int(contents)
        except:
            self.high_score = 0
        


screen.tracer(0)
snake = Snake()
food = Food()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(snake.up, 'Up')
screen.onkey(snake.down, 'Down')
screen.onkey(snake.left, 'Left')
screen.onkey(snake.right, 'Right')

game_over = True
def reset_game():
    global game_over, scoreboard, snake
    if game_over:
        snake.reset()
        scoreboard.reset()
        return game_loop()

def quit_game():
    exit()

screen.onkey(reset_game, 'r')
screen.onkey(quit_game, 'q')
# game_is_on = True

def game_loop():
    game_over = False
    while True:
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
            # game_is_on = False
            game_over = True
            scoreboard.game_over()
            return

game_loop()

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


