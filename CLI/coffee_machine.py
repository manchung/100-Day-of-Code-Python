import os 

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

logo = '''
________._________
|      | \   -   /
|  ||  |  \  -  /
|  ||  |___\___/
|  ||  |     X
|      |    ___
|      |   / - \\
|______|  /  -  \\
| ____ | /_______\\
||7:30||__________
||____|           |
|_________________|
'''

money = 0

def print_report():
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${money}")

def transact_coffee(flavor):
    resource = check_missing_resource(flavor)
    if resource is not None:
        print(f"Sorry there is not enough {resource}.")
        return

    cost = MENU[flavor]['cost']
    payment = get_money(flavor)
    if payment < cost:
        refund()
    else:
        if payment > cost: 
            make_change(cost, payment)
        global money
        money += cost
        deduct_resources(flavor)
        make_coffee(flavor)

def check_missing_resource(flavor):
    for r in MENU[flavor]["ingredients"]:
        if resources[r] < MENU[flavor]["ingredients"][r]:
            return r
    return None

def make_change(cost, payment):
    print(f"Here is ${format(round(payment - cost, 2), '.2f')} dollars in change")

def get_money(flavor):
    print("Please insert coins.")
    quarters = int(input("How many quarters? "))
    dimes = int(input("How many dimes? "))
    nickles = int(input("How many nickles? "))
    pennies = int(input("How many pennies? "))
    money = 0.25 * quarters + 0.10 * dimes + 0.05 * nickles + 0.01 * pennies
    return money

def deduct_resources(flavor):
    for r in MENU[flavor]["ingredients"]:
        resources[r] -= MENU[flavor]["ingredients"][r]

def make_coffee(flavor):
    print(f"Here is your ☕ {flavor}. Enjoy!")
          
def refund():
    print("Sorry that's not enough money. Money refunded.")

os.system('clear')
print(logo)
still_running = True
while still_running:
    ans = input("What would you like? (espresso/latte/cappuccino): ")
    if ans == "report":
        print_report()
    elif ans == "off":
        still_running = False
    elif ans in ['espresso', 'latte', 'cappuccino']:
        transact_coffee(ans)
    else:
        print("Unrecognized input. Try again.")



 

