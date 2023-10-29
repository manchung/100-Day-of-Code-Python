import os

logo = '''
                         ___________
                         \         /
                          )_______(
                          |"""""""|_.-._,.---------.,_.-._
                          |       | | |               | | ''-.
                          |       |_| |_             _| |_..-'
                          |_______| '-' `'---------'` '-'
                          )"""""""(
                         /_________\\
                       .-------------.
                      /_______________\\
'''

print(logo)
print("Welcome to the secret auction program.")

bids = {}
more_bidder = True

while more_bidder:
    name = input("What is your name?: ")
    bid = int(input("What's your bid?: $"))
    bids[name] = bid
    answer = input("Are there any other bidders? Type 'yes' or 'no'. ")
    if answer == 'no':
        more_bidder = False
    os.system("clear")

winning_bid = []
for bidder in bids:
    if len(winning_bid) == 0:
        winning_bid = [bidder, bids[bidder]]
    elif bids[bidder] > winning_bid[1]:
        winning_bid = [bidder, bids[bidder]]

print(f"The winner is {winning_bid[0]} with a bid of ${winning_bid[1]}")

