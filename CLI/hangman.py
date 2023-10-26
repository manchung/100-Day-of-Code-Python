import random
import os
from hangman_art import *
from hangman_words import word_list

chosen_word = random.choice(word_list).lower()
display = list("_" * len(chosen_word))

#print(f"Secret.... chosen_word: {chosen_word}")

lives = 6
continue_game = True

guesses = []
os.system('clear')
print(logo)
while continue_game:
    guess = input("Guess a letter: ").lower()
    os.system('clear')
    print("---------------")
    guess_correct = False
    for i in range(len(chosen_word)):
        letter = chosen_word[i]
        if guess == letter:
            display[i] = guess
            guess_correct = True
    
    if guess in guesses:
        print(f"You already guessed {guess}")
    elif not guess_correct:
        lives -= 1
        print(f"You guessed {guess}, that's not in the word. You lose a life.")
    
    guesses += guess
    print(stages[lives])
    print(" ".join(display))
    continue_game = lives > 0 and "_" in display

if lives > 0:
    print("You won")
else:
    print(f"You lost. The correct word is {chosen_word}")
