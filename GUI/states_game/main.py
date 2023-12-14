import turtle, csv

image = 'blank_states_img.gif'
state_csv_filename = '50_states.csv'

# Change screen to blank state map
screen = turtle.Screen()
screen.title('US States Game')
screen.addshape(image)
turtle.shape(image)

# read in csv file
state_coords = {}

with open(state_csv_filename, 'r') as file:
    csv_file = csv.reader(file)
    next(csv_file)  # skips header
    for line in csv_file:
        state = line[0].lower()
        coords = (int(line[1]), int(line[2]))
        state_coords[state] = coords

screen.onkey(exit, 'q')

states_guessed_right = []

write_turtle = turtle.Turtle()
write_turtle.penup()
write_turtle.hideturtle()
turtle_font = ('Arial', 10, 'normal')

def game_loop():
    game_over = False
    title = 'Guess the State'
    prompt = "What's another state's name?"
    while True:
        answer = screen.textinput(title=title, prompt=prompt)
        if answer is None: continue
        lower_answer = answer.lower()
        if lower_answer == 'exit':
            break
        if lower_answer in states_guessed_right or \
            lower_answer not in state_coords:
            continue
        states_guessed_right.append(lower_answer)
        coords = state_coords[lower_answer]
        write_turtle.goto(*coords)
        write_turtle.write(lower_answer.title(), font=turtle_font)
        title = f'{len(states_guessed_right)}/50 states correct'
        if len(states_guessed_right) == 50:
            break

game_loop()
states_missed = list(state_coords.keys() - states_guessed_right)
states_missed.sort()

with open('missed_states.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['state'])
    for state in states_missed:
        writer.writerow([state.title()])

# screen.exitonclick()