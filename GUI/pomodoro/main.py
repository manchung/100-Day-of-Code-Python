from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
# WORK_MIN = 0.2
SHORT_BREAK_MIN = 5
# SHORT_BREAK_MIN = 0.1
LONG_BREAK_MIN = 20
# LONG_BREAK_MIN = 0.2
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps
    reps = 0
    window.after_cancel(timer)
    timer_label.config(text='Timer', fg=GREEN)
    canvas.itemconfig(canvas_text, text='00:00')
    checkmark_label.config(text='')

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps, WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN
    if reps == 7:
        seconds = LONG_BREAK_MIN * 60
        timer_label.config(text='Break', fg=RED)
        reps = 0
    elif reps in [0, 2, 4, 6]:
        seconds = WORK_MIN * 60
        timer_label.config(text='Work', fg=GREEN)
        reps += 1
    elif reps in [1, 3, 5]:
        seconds = SHORT_BREAK_MIN * 60
        timer_label.config(text='Break', fg=PINK)
        reps += 1
    
    num_checkmarks = int(reps / 2) + 1
    count_down(int(seconds), num_checkmarks)
    

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count, num_checkmarks):
    global timer
    minute = int(count / 60)
    seconds = count % 60
    canvas.itemconfig(canvas_text, text=f'{minute}:{seconds:02d}')
    if count > 0:
        timer = window.after(1000, count_down, count-1, num_checkmarks)
    elif count == 0:
        checkmark_label.config(text='✓'*num_checkmarks)
        start_timer()
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Pomodoro')
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file='tomato.png')
canvas.create_image(100, 112, image=tomato_img)
canvas_text = canvas.create_text(100,130, text='00:00', fill='white', font=(FONT_NAME,35,'bold'))
canvas.grid(row=1, column=1)

timer_label = Label(text='Timer', fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, 'normal'))
timer_label.grid(row=0, column=1, pady=(0,20))

start_button = Button(text='Start', highlightthickness=0, highlightbackground=YELLOW, 
                      font=('Arial', 20, 'normal'), command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text='Reset', highlightthickness=0, highlightbackground=YELLOW,
                      font=('Arial', 20, 'normal'), command=reset_timer)
reset_button.grid(row=2, column=2)

# checkmark_label = Label(text='✓', fg=GREEN, bg=YELLOW, font=('Arial', 35, 'bold'))
checkmark_label = Label(text='', fg=GREEN, bg=YELLOW, font=('Arial', 35, 'bold'))
checkmark_label.grid(row=3, column=1)


window.mainloop()