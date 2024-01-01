from tkinter import *
import os
from functools import partial
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

class QuizzlerInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz_brain = quiz_brain
        self.build_ui()
        self.get_next_question()
        self.window.mainloop()

    def build_ui(self):
        self.window = Tk()
        self.window.title('Quizzler')
        self.window.config(background=THEME_COLOR, padx=20, pady=20)

        self.score_label = Label(text='Score: 0', fg='white', bg=THEME_COLOR)
        self.score_label.grid(row=0, column=1, pady=20)

        self.canvas = Canvas(width=300, height=250, background='white', highlightthickness=0)
        self.canvas_text = self.canvas.create_text(150, 125, text="Question???", 
                                                   width=280, font=("Arial", 20, "italic"), fill="black")
        self.canvas.grid(row=1, column=0, columnspan=2, pady=20)

        true_img_filename = os.path.join(os.path.dirname(__file__), 'images', 'true.png')
        false_img_filename = os.path.join(os.path.dirname(__file__), 'images', 'false.png')
        # print(f'true_img_filename: {true_img_filename}')
        # print(f'false_img_filename: {false_img_filename}')

        self.correct_button_img = PhotoImage(file=true_img_filename)
        self.correct_button = Button(image=self.correct_button_img, highlightthickness=0, 
                                     bg=THEME_COLOR, command=partial(self.check_answer, answer='true'))
        self.correct_button.grid(row=2, column=0, pady=(20,0))

        self.wrong_button_img = PhotoImage(file=false_img_filename)
        self.wrong_button = Button(image=self.wrong_button_img, highlightthickness=0, 
                                   bg=THEME_COLOR, command=partial(self.check_answer, answer='false'))
        self.wrong_button.grid(row=2, column=1, pady=(20,0))
    
    def get_next_question(self):
        if self.quiz_brain.still_has_questions():
            question_text = self.quiz_brain.next_question()
        else:
            question_text = f"Game over. Final score {self.quiz_brain.score}. Press any button to quit."
            self.correct_button.config(command=self.quit)
            self.wrong_button.config(command=self.quit)
        self.canvas.itemconfig(self.canvas_text, text=question_text)
    
    def check_answer(self, answer: str):
        is_right = self.quiz_brain.check_answer(answer)
        if is_right:
            self.canvas.config(background='green')
        else:
            self.canvas.config(background='red')
        self.window.after(1000, partial(self.canvas.config, background='white'))
        self.window.after(1000, self.update_score)
        self.window.after(1000, self.get_next_question)

    def update_score(self):
        score = self.quiz_brain.score
        self.score_label.config(text=f'Score: {score}')
    
    def quit(self):
        exit(0)