print("Welcome to the tip calculator.")
bill_amount = float(input("What was the total bill? $"))
tip_percent = float(input("What percentage tip would you like to give? 10, 12, or 15? "))
num_people = int(input("How many people to split the bill? "))

bill_amount *= (1 + tip_percent/100)
each_pay = "%.2f" % round(bill_amount / num_people, 2)
print(f"Each person should pay: ${each_pay}")
