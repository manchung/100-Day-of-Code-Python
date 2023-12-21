from tkinter import *
from tkinter import messagebox
import os, csv, random


BACKGROUND_COLOR = "#B1DDC6"
LANG_TEXT_FONT = ('Ariel', 40, 'italic')
WORD_TEXT_FONT = ('Ariel', 60, 'bold')

window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card_front_img = PhotoImage(file=f'{os.path.dirname(__file__)}/images/card_front.png')
card_back_img = PhotoImage(file=f'{os.path.dirname(__file__)}/images/card_back.png')
right_img = PhotoImage(file=f'{os.path.dirname(__file__)}/images/right.png')
wrong_img = PhotoImage(file=f'{os.path.dirname(__file__)}/images/wrong.png')
french_words_filename = f'{os.path.dirname(__file__)}/data/french_words.csv'
words_to_learn_filename = f'{os.path.dirname(__file__)}/data/words_to_learn.csv'

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_card = canvas.create_image(400, 263, image=card_front_img)
canvas_lang_text = canvas.create_text(400,150, text='', fill='black', font=LANG_TEXT_FONT)
canvas_word_text = canvas.create_text(400,263, text='', fill='black', font=WORD_TEXT_FONT)
canvas.grid(row=0, column=0, columnspan=2)

wrong_button = Button(image=wrong_img, highlightthickness=0, highlightbackground=BACKGROUND_COLOR)
wrong_button.grid(row=1, column=0)

right_button = Button(image=right_img, highlightthickness=0, highlightbackground=BACKGROUND_COLOR)
right_button.grid(row=1, column=1)

all_words_list = []
words_list = []

try:
    with open(words_to_learn_filename, 'r') as file:
        dictR = csv.DictReader(file)
        for line in dictR:
            words_list.append(list(line.values()))
except FileNotFoundError:
    pass

try: 
    with open(french_words_filename, 'r') as file:
        dictR = csv.DictReader(file)
        for line in dictR:
            all_words_list.append(list(line.values()))
except FileNotFoundError:
    messagebox.showerror(title='Error', message=f'Cannot find word file {french_words_filename}')

if len(words_list) == 0:
    words_list = all_words_list

flip_timer = None
current_words = None
def new_front_card():
    global flip_timer, current_words, words_list
    if flip_timer is not None:
        window.after_cancel(flip_timer)
    
    if len(words_list) == 0:
        words_list = all_words_list
    current_words = random.choice(words_list)
    # print(f'current_words: {current_words}')
    canvas.itemconfig(canvas_lang_text, text='French', fill='black')
    canvas.itemconfig(canvas_word_text, text=current_words[0], fill='black')
    canvas.itemconfig(canvas_card, image=card_front_img)
    flip_timer = window.after(3000, new_back_card)

def new_back_card():
    global current_words
    canvas.itemconfig(canvas_lang_text, text='English', fill='white')
    canvas.itemconfig(canvas_word_text, text=current_words[1], fill='white')
    canvas.itemconfig(canvas_card, image=card_back_img)

def answer_right():
    global words_list
    words_list.remove(current_words)
    # print(f'words_list count: {len(words_list)}')
    save_file()
    new_front_card()

def save_file():
    with open(words_to_learn_filename, 'w') as file:
        fieldnames = ['French', 'English']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for french, english in words_list:
            writer.writerow({'French': french, 'English': english})

wrong_button.config(command=new_front_card)
right_button.config(command=answer_right)

new_front_card()


window.mainloop()