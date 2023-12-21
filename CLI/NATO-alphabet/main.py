import pandas as pd
import os

nato_filename = f'{os.path.dirname(__file__)}/nato_phonetic_alphabet.csv'
df = pd.read_csv(nato_filename)


#TODO 1. Create a dictionary in this format:
# {"A": "Alfa", "B": "Bravo"}
nato_dict = {row.letter:row.code for (index, row) in df.iterrows()} 

#TODO 2. Create a list of the phonetic code words from a word that the user inputs.
loop = True

while loop:
    text = input('Enter a word: ')
    try:
        print([nato_dict[letter] for letter in text.upper()])
    except KeyError:
        print('Sorry, only letters in the alphabet please.')
    else: 
        loop = False

