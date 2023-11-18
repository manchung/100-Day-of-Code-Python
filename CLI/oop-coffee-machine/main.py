from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine
import os

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

menu = Menu()
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()

os.system('clear')
print(logo)
still_running = True
while still_running:
    ans = input(f"What would you like? ({menu.get_items()}): ")
    if ans == "report":
        coffee_maker.report()
        money_machine.report()
    elif ans == "off":
        still_running = False
    elif ans in menu.get_items().split('/') and len(ans) > 0:
        # transact_coffee(ans)
        menu_item = menu.find_drink(ans)
        if not coffee_maker.is_resource_sufficient(menu_item):
            continue
        
        cost = menu_item.cost
        payment_succeed = money_machine.make_payment(cost)

        if payment_succeed:
            coffee_maker.make_coffee(menu_item)
    else:
        print("Unrecognized input. Try again.")



