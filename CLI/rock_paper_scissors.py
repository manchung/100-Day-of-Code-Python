import random

rock_img = """
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
"""

paper_img = """
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
"""

scissors_img = """
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""

images = [rock_img, paper_img, scissors_img]

user_choice = input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors.\n")
if user_choice not in ["0", "1", "2"]:
    print("Invalid choice. Please input 0, 1 or 2")
    exit(0)

user_choice = int(user_choice)
computer_choice = random.randint(0,2)

# game_outcome: 0 - draw, 1 - user wins, 2 - computer wins
game_outcome = 0

if user_choice == 0:
    if computer_choice == 1:
        game_outcome = 2
    elif computer_choice == 2:
        game_outcome = 1
elif user_choice == 1:
    if computer_choice == 0:
        game_outcome = 1
    elif computer_choice == 2:
        game_outcome = 2
else:
    if computer_choice == 0:
        game_outcome = 2
    elif computer_choice == 1:
        game_outcome = 1

print(images[user_choice])
print("\nComputer chose:\n")
print(images[computer_choice])

if game_outcome == 0:
    print("Game is drawn")
elif game_outcome == 1:
    print("You win")
else:
    print("You lose")