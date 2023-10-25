import random
import string

print("Welcome to the PyPassword Generator!")
num_letters = int(input("How many letters would you like in your password?\n"))
num_symbols = int(input("How many symbols would you like?\n"))
num_numbers = int(input("How many numbers would you like?\n"))

letters = list(string.ascii_letters)
numbers = list(string.digits)
symbols = list('!@#$%^&*()')

password = []
for i in range(num_letters):
    password.append(random.choice(letters))

for i in range(num_numbers):
    password.append(random.choice(numbers))

for i in range(num_symbols):
    password.append(random.choice(symbols))

random.shuffle(password)
print(f"Here is your password {''.join(password)}")                

