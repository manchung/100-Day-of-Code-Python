import random, os

logo = """
    __  ___       __             
   / / / (_)___ _/ /_  ___  _____
  / /_/ / / __ `/ __ \/ _ \/ ___/
 / __  / / /_/ / / / /  __/ /    
/_/ ///_/\__, /_/ /_/\___/_/     
   / /  /____/_      _____  _____
  / /   / __ \ | /| / / _ \/ ___/
 / /___/ /_/ / |/ |/ /  __/ /    
/_____/\____/|__/|__/\___/_/     
"""

vs = """
 _    __    
| |  / /____
| | / / ___/
| |/ (__  ) 
|___/____(_)
"""

from higher_lower_game_data import data


score = 0
curr = random.choice(data)
continue_game = True

while continue_game:
    os.system('clear')
    print(logo)
    if score > 0:
        print(f"You're right! Current score: {score}")
    
    print(f"Compare A: {curr['name']}, a {curr['description']}, from {curr['country']}.")
    print(vs)

    next = random.choice(data)
    while next['name'] == curr['name']:
        next = random.choice(data)

    print(f"Against B: {next['name']}, a {next['description']}, from {next['country']}.")
    ans = input("Who has more followers? Type 'A' or 'B': ")

    if ans == 'A' and curr['follower_count'] > next['follower_count']:
        score += 1
    elif ans == 'B' and next['follower_count'] > curr['follower_count']:
        curr = next
        score += 1
    else:
        continue_game = False

print(f"Sorry, that's wrong. Final score: {score}")



