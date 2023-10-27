import string
from art import logo

alphabet = list(string.ascii_lowercase)

def caesar(text, shift, direction):
    result_text = ""
    for letter in text:
        if letter in alphabet:
            pos = alphabet.index(letter)
            if direction == "encode":
                shifted_pos = (pos + shift) % len(alphabet)
            else:
                shifted_pos = (pos - shift) % len(alphabet)
            result_text += alphabet[shifted_pos]
        else:
            result_text += letter

    print(f"The {direction}d text is {result_text}")

print(logo)
run_again = True

while run_again:
    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
    text = input("Type your message:\n").lower()
    shift = int(input("Type your shift number:\n"))
    caesar(text, shift, direction)
    to_run_again = input("Type 'yes' if you want to go again. Otherwise type 'no'.\n")
    if to_run_again == 'yes':
        run_again = True
    else:
        run_again = False
        print("Goodbye")

