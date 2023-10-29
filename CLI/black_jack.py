import os, random

logo = """
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\
      |  \/ K|                            _/ |                
      `------'                           |__/           
"""
                   

cards = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']

def deal_card():
    return random.choice(cards)

def show_cards(player_cards, dealer_cards, reveal_all=False):
    player_sums = sum_cards(player_cards)
    if all_over_21(player_sums):
        player_max = max(player_sums)
    else:
        player_max = max(map(close_to_21, player_sums))
    print(f"    Your cards: {player_cards}, current scores: {player_max}")
    if reveal_all:
        dealer_sums = sum_cards(dealer_cards)
        if all_over_21(dealer_sums):
            dealer_max = max(dealer_sums)
        else:
            dealer_max = max(map(close_to_21, dealer_sums))
        print(f"    Computer cards: {dealer_cards}, computer score: {dealer_max}")
    else:
        print(f"    Computer's first card [{dealer_cards[0]}] of total {len(dealer_cards)} cards")


# return a list of possible sums
def sum_cards(cards):
    def running_sum(res, remaining_cards):
        if len(remaining_cards) == 0:
            return res;
        
        if remaining_cards[0] == 'A':
            # need to double the result list 
            res = list(map(lambda x: x + 1, res)) + list(map(lambda x: x + 11, res))
        elif remaining_cards[0] in ['J', 'Q', 'K']:
            res = list(map(lambda x: x + 10, res))
        else:
            res = list(map(lambda x: x + remaining_cards[0], res))
        return running_sum(res, remaining_cards[1:])
    return running_sum([0], cards)

def dealer_under_17(cards):
    sum = 0
    for c in cards:
        if c == 'A':
            sum += 11
        elif c == 'J' or c == 'Q' or c == 'K':
            sum += 10
        else:
            sum += int(c)
    return sum < 17

def close_to_21(x):
    if x <= 21:
        return x
    else:
        return 0

def all_over_21(sums):
    for s in sums:
        if s <= 21:
            return False
    return True

def play_game():
    player_cards = [deal_card(), deal_card()]
    dealer_cards = [deal_card(), deal_card()]

    show_cards(player_cards, dealer_cards)
    winner = ""
    game_over = False

    player_sums = sum_cards(player_cards)
    dealer_sums = sum_cards(dealer_cards)
    if 21 in player_sums:
        winner = "You"
        game_over = True
    elif 21 in dealer_sums:
        winner = "Computer"
        game_over = True
    
    while not game_over:        
        another_card = input("Type 'y' to get another card, type 'n' to pass: ")
        if another_card == 'y':
            player_cards.append(deal_card())
        
        if dealer_under_17(dealer_cards):
            print("    Dealer under 17. Dealer get one more card.")
            dealer_cards.append(deal_card())
        
        player_sums = sum_cards(player_cards)
        # player bust if every sum is > 21
        if all_over_21(player_sums):
            print("You went over. You lose.")
            winner = "Computer"
            game_over = True
        elif 21 in player_sums and len(player_cards) == 2:
            winner = "You"
            game_over = True
        elif another_card == 'n': 
            while dealer_under_17(dealer_cards):
                print("    Dealer under 17. Dealer get one more card.")
                dealer_cards.append(deal_card())
            
            dealer_sums = sum_cards(dealer_cards)
            if all_over_21(dealer_sums):
                print("Computer went over. Computer loses.")
                # print(f"dealer sums = {dealer_sums}")
                winner = "You"
            elif 21 in dealer_sums and len(dealer_cards) == 2:
                winner = "Computer"
            else:
                # need to see which one has cards closest to 21
                player_max = max(map(close_to_21, player_sums))
                dealer_max = max(map(close_to_21, dealer_sums))
                # print(f"player_max = {player_max}, dealer_max = {dealer_max}")
                if player_max > dealer_max:
                    winner = "You"
                elif player_max < dealer_max:
                    winner = "Computer"
                else: 
                    winner = "Draw"
            game_over = True
        if not game_over:
            show_cards(player_cards, dealer_cards)
    
    show_cards(player_cards, dealer_cards, reveal_all=True)
    if winner == "Draw":
        print("Game is drawn")
    else:
        print(f"Winner is {winner}")
    return winner

scores = {
    "You": 0,
    "Computer": 0,
    "Draw": 0
}

should_continue = True
while should_continue:
    os.system("clear")
    print(logo)
    winner = play_game()
    scores[winner] += 1
    next_game_query = input("Do you want to play a game of Blackjack? Type 'y' or 'n': " )
    if next_game_query == 'n':
        should_continue = False
        
print(f"Final scores:\n   You win {scores['You']} games\n   Computer win {scores['Computer']} games\n   Draws {scores['Draw']} games")