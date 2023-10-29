import random, os

logo = """

 .oOOOo.                                 oOoOOoOOo  o                o.     O                  o                 
.O     o                                     o     O                 Oo     o                 O                  
o                                            o     o                 O O    O                 O                  
O                                            O     O                 O  o   o                 o                  
O   .oOOo O   o  .oOo. .oOo  .oOo            o     OoOo. .oOo.       O   o  O O   o  `oOOoOO. OoOo. .oOo. `OoOo. 
o.      O o   O  OooO' `Ooo. `Ooo.           O     o   o OooO'       o    O O o   O   O  o  o O   o OooO'  o     
 O.    oO O   o  O         O     O           O     o   O O           o     Oo O   o   o  O  O o   O O      O     
  `OooO'  `OoO'o `OoO' `OoO' `OoO'           o'    O   o `OoO'       O     `o `OoO'o  O  o  o `OoO' `OoO'  o     
                                                                                                                                                                                                                                
"""

def guess_game(num_attempts):
    key = random.randint(1, 100)
    while num_attempts > 0:
        print(f"You have {num_attempts} remaining to guess the number")
        guess = int(input("Make a guess: "))
        if guess == key:
            print("You made the right guess! You win.")
            break
        elif guess > key:
            print("Too high.")
            print("Guess again.")
        else:
            print("Too low.")
            print("Guess again.")
        num_attempts -= 1
    if num_attempts == 0:
        print("You've run out of guesses. You lose.")
        print(f"The correct answer is {key}")

os.system('clear')
print(logo)
print("Welcoem to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")

diff_level = input("Choose a difficulty. Type 'easy' or 'hard': ")
if diff_level == "hard":
    guess_game(5)
else:
    guess_game(10)
