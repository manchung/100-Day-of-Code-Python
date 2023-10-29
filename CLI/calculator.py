import os

logo = """
 _____________________
|  _________________  |
| | Pythonista   0. | |  .----------------.  .----------------.  .----------------.  .----------------. 
| |_________________| | | .--------------. || .--------------. || .--------------. || .--------------. |
|  ___ ___ ___   ___  | | |     ______   | || |      __      | || |   _____      | || |     ______   | |
| | 7 | 8 | 9 | | + | | | |   .' ___  |  | || |     /  \     | || |  |_   _|     | || |   .' ___  |  | |
| |___|___|___| |___| | | |  / .'   \_|  | || |    / /\ \    | || |    | |       | || |  / .'   \_|  | |
| | 4 | 5 | 6 | | - | | | |  | |         | || |   / ____ \   | || |    | |   _   | || |  | |         | |
| |___|___|___| |___| | | |  \ `.___.'\  | || | _/ /    \ \_ | || |   _| |__/ |  | || |  \ `.___.'\  | |
| | 1 | 2 | 3 | | x | | | |   `._____.'  | || ||____|  |____|| || |  |________|  | || |   `._____.'  | |
| |___|___|___| |___| | | |              | || |              | || |              | || |              | |
| | . | 0 | = | | / | | | '--------------' || '--------------' || '--------------' || '--------------' |
| |___|___|___| |___| |  '----------------'  '----------------'  '----------------'  '----------------' 
|_____________________|
"""

operations = "+-*/"
def print_ops(ops):
    for c in ops:
        print(c)

def calculate(prev_result=None):
    if prev_result is None:
        num_1 = float(input("What's your first number?: "))
    else:
        num_1 = prev_result
    print_ops(operations)
    op = input("Pick an operation: ")
    num_2 = float(input("What's your next number?: "))
    res = eval(f"{num_1} {op} {num_2}")
    print(f"{num_1} {op} {num_2} = {res}")
    return res

os.system("clear")
print(logo)
res = calculate(prev_result=None)

should_continue = True
while should_continue:
    ans = input(f"Type 'y' to continue calculating with {res}, or \ntype 'n' to start a new calculation, or \ntype 'q' to quit: ")
    if ans == "q":
        should_continue = False
    elif ans == "y":
        res = calculate(res)
    else:
        os.system("clear")
        print(logo)
        res = calculate(None)

