from turtle import Turtle, Screen
import time

SCREEN_SIZE = (800, 600)

class Paddle(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape('square')
        self.color('white')
        self.penup()
        self.goto((x, y))
        self.resizemode('user')
        self.setheading(90)
        self.shapesize(stretch_len=5, stretch_wid=1)
    
    def up(self):
        # self.setheading(90)
        self.forward(20)
    
    def down(self):
        # self.setheading(270)
        self.forward(-20)

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.inc_x = 10
        self.inc_y = 10
        self.speed_factor = 1.0
        self.shape('circle')
        self.color('white')
        self.penup()
        self.goto(0,0)
    
    def move(self):
        new_x = self.xcor() + self.inc_x * self.speed_factor
        new_y = self.ycor() + self.inc_y * self.speed_factor
        self.goto(new_x, new_y)
    
    def bounce_x(self):
        self.inc_x *= -1
    
    def bounce_y(self):
        self.inc_y *= -1
    
    def reset(self):
        self.goto(0,0)
        self.speed_factor = 1
        self.inc_x *= -1
    
    def heading_right(self):
        return self.inc_x > 0
    
    def inc_speed(self):
        self.speed_factor *= 1.1
        # print(f"New speed: {self.speed_factor}")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.left_score = 0
        self.right_score = 0
        self.game_is_paused = False
        self.game_is_on = True
        self.pencolor('white')
        self.penup()
        self.write_score()
        self.hideturtle()
    
    def write_score(self):
        self.clear()
        self.goto(0,280)
        self.write(f"{self.left_score}  Score  {self.right_score}", align='center', font=('Courier', 20, 'bold'))
        self.goto(0,-290)
        self.write("Press <p> to Pause, <q> to Quit", align='center', font=('Courier', 10, 'normal'))

    def reset(self):
        self.left_score = 0
        self.right_score = 0
        self.write_score()

    def inc_left(self):
        self.left_score += 1
        self.write_score()
    
    def inc_right(self):
        self.right_score += 1
        self.write_score()
    
    def pause_game(self):
        self.game_is_paused = not self.game_is_paused
        # print(f"game_is_paused: {self.game_is_paused}")
    
    def quit_game(self):
        self.game_is_on = False
    
    def is_game_on(self):
        return self.game_is_on
    
    def is_game_paused(self):
        return self.game_is_paused
        
    
screen = Screen()
screen.setup(width=SCREEN_SIZE[0], height=SCREEN_SIZE[1])
screen.bgcolor('black')
screen.title('Pong')
screen.tracer(0)

r_paddle = Paddle(350, 0)
l_paddle = Paddle(-350, 0)
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkeypress(r_paddle.up, 'Up')
screen.onkeypress(r_paddle.down, 'Down')
screen.onkeypress(l_paddle.up, 'w')
screen.onkeypress(l_paddle.down, 's')
screen.onkeypress(scoreboard.pause_game, 'p')
screen.onkeypress(scoreboard.quit_game, 'q')

while scoreboard.is_game_on():
    time.sleep(0.1)
    screen.update()
    if scoreboard.is_game_paused():
        # time.sleep(1)
        continue
    if ball.ycor() >= 280 or ball.ycor() <= -280:
        ball.bounce_y()
    
    if ball.xcor() >= 330 and ball.distance(r_paddle) <= 50 and ball.heading_right():
        ball.bounce_x()
        ball.inc_speed()
    elif ball.xcor() <= -330 and ball.distance(l_paddle) <= 50 and not ball.heading_right():
        ball.bounce_x()
        ball.inc_speed()
    
    if ball.xcor() > 400:
        ball.reset()
        scoreboard.inc_left()
    
    if ball.xcor() < -400:
        ball.reset()
        scoreboard.inc_right()

    ball.move()
    

# screen.exitonclick()
