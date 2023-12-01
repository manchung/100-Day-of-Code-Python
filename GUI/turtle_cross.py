from turtle import Turtle, Screen
import time, random

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.inc_y = 20
        self.shape('turtle')
        self.penup()
        self.color('black')
        self.setheading(90)
        self.goto(0, -270)
    
    def up(self):
        self.goto(x=self.xcor(), y=self.ycor()+self.inc_y)

    def reset(self):
        self.goto(0, -270)

class CarManager:
    colors = ['red', 'purple', 'orange', 'pink', 'blue', 'yellow', 'green']
    y_tracks = range(-240, 240, 20)
    # x_tracks = range(320, 350, 5)
    # xy_tracks = [(x, y) for x in range(320, 350, 5) for y in range(-250, 260, 20)]
    def __init__(self):
        self.car_create_prob = 0.3
        self.car_inc_x = -10
        self.cars = []
        self.last_created_5y = [None] * 5
    
    def create_car(self):
        car = Turtle()
        car.shape('square')
        car.setheading(270)
        car.penup()
        car.shapesize(stretch_len=1, stretch_wid=3)
        car.color(random.choice(CarManager.colors))

        y = random.choice(CarManager.y_tracks)
        while y in self.last_created_5y:
            y = random.choice(CarManager.y_tracks)
        self.last_created_5y.pop(0)
        self.last_created_5y.append(y)

        car.goto(310, y)
        self.cars.append(car)
    
    def move_cars(self):
        to_remove = []
        for car in self.cars:
            if car.xcor() < -350:
                to_remove.append(car)
            else:
                car.goto(x=car.xcor()+self.car_inc_x, y=car.ycor())
        
        # print(f"before remove number of cars: {len(self.cars)}")
        for car in to_remove:
            self.cars.remove(car)
        # print(f"after remove number of cars: {len(self.cars)}")

        if random.random() < self.car_create_prob:
            self.create_car()

    def collide(self, turtle):
        turtle_x = turtle.xcor()
        turtle_y = turtle.ycor()
        for car in self.cars:
            car_x = car.xcor()
            car_y = car.ycor()
            if abs(car_y - turtle_y) < 20 and abs(car_x - turtle_x) < 50 and turtle_x < car_x:
                return True
    
    def inc_difficulty(self):
        self.car_create_prob *= 1.1
        self.car_inc_x *= 1.1
        # print(f"car_create_prob: {self.car_create_prob}  car_inc_x: {self.car_inc_x}")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.game_is_paused = False
        self.game_is_on = True
        self.pencolor('black')
        self.penup()
        self.write_score()
        self.hideturtle()
    
    def write_score(self):
        self.clear()
        self.goto(-280,280)
        self.write(f"Level:  {self.level}", align='left', font=('Courier', 20, 'bold'))
        self.goto(0,-290)
        self.write("Press <p> to Pause, <q> to Quit", align='center', font=('Courier', 10, 'normal'))

    
    def pause_game(self):
        self.game_is_paused = not self.game_is_paused
        # print(f"game_is_paused: {self.game_is_paused}")
    
    def quit_game(self):
        self.game_is_on = False
    
    def is_game_on(self):
        return self.game_is_on
    
    def is_game_paused(self):
        return self.game_is_paused
    
    def game_over(self):
        self.goto(0,0)
        self.write('GAME OVER', align='center', font=('Courier', 40, 'bold'))
        self.pause_game()
    
    def inc_level(self):
        self.level += 1
        self.write_score()
        

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor('white')
screen.title('Turtle Crossing')
screen.tracer(0)

scoreboard = Scoreboard()
player = Player()
car_manager = CarManager()
car_manager.create_car()
car_manager.create_car()

screen.listen()
screen.onkeypress(player.up, 'Up')
screen.onkeypress(scoreboard.pause_game, 'p')
screen.onkeypress(scoreboard.quit_game, 'q')

while scoreboard.is_game_on():
    time.sleep(0.1)
    screen.update()
    if scoreboard.is_game_paused():
        # time.sleep(1)
        continue

    car_manager.move_cars()
    if car_manager.collide(player):
        # print('collide')
        scoreboard.game_over()
    
    if player.ycor() > 290:
        scoreboard.inc_level()
        car_manager.inc_difficulty()
        player.reset()


