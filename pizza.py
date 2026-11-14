pizza_prices = {
    "Small":  {"Veg": 149, "Non-Veg": 199},
    "Medium": {"Veg": 249, "Non-Veg": 299},
    "Large":  {"Veg": 349, "Non-Veg": 399}
}
pizza_flavours = {
    "Veg": ["Margherita", "Farmhouse", "Veggie Delight"],
    "Non-Veg": ["Chicken Tikka", "Pepperoni", "BBQ Chicken"]
}
base_prices = {
    "Classic": 0,
    "Thin Crust": 30,
    "Cheese Burst": 60
}
topping_prices = {
    "Extra Cheese": 40,
    "Extra Veggies": 30
}
menu = {
    "Drinks": {
        "Coke": 50,
        "Lemonade": 40,
        "Cold Coffee": 80
    },

    "Snacks": {
        "Garlic Bread": 100,
        "French Fries": 90,
        "Veg Nuggets": 110
    },

    "Desserts": {
        "Brownie": 90,
        "Ice Cream": 70,
        "Chocolate Cake": 120
    }
}
def show_menu(items):
    for number, item in enumerate(items, start=1):
        print(f"{number}. {item}")
def get_choice(items, message):
    items_list = list(items)
    while True:
        show_menu(items_list)

        choice = input(message)

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(items_list):
                return items_list[choice - 1]
        print("Invalid choice! Please try again.\n")
def ask_yes_no(message):
    while True:
        answer = input(message).strip().lower()

        if answer in ["yes", "y"]:
            return True
        elif answer in ["no", "n"]:
            return False
        else:
            print("Please enter yes or no.")
bill_items = []
print("=" * 45)
print("          WELCOME TO PYTHON PIZZA")
print("=" * 45)
customer_name = input("Enter your name: ").strip()

if not customer_name:
    customer_name = "Customer"
while True:

    print("\n========== PIZZA MENU ==========")


    size = get_choice(
        pizza_prices.keys(),
        "Choose pizza size (enter number): "
    )

    pizza_type = get_choice(
        pizza_flavours.keys(),
        "Choose pizza type (enter number): "
    )

  
    flavour = get_choice(
        pizza_flavours[pizza_type],
        "Choose pizza flavour (enter number): "
    )


    base = get_choice(
        base_prices.keys(),
        "Choose pizza base (enter number): "
    )

    pizza_cost = pizza_prices[size][pizza_type]
    pizza_cost += base_prices[base]

    if ask_yes_no("Do you want extra cheese? (yes/no): "):
        pizza_cost += topping_prices["Extra Cheese"]
        cheese = "Yes"
    else:
        cheese = "No"

 
    if ask_yes_no("Do you want extra veggies? (yes/no): "):
        pizza_cost += topping_prices["Extra Veggies"]
        veggies = "Yes"
    else:
        veggies = "No"

  
    while True:
        quantity = input("Enter pizza quantity: ")

        if quantity.isdigit() and int(quantity) > 0:
            quantity = int(quantity)
            break

        print("Please enter a positive whole number.")

  
    total_pizza_cost = pizza_cost * quantity


    pizza_name = f"{size} {pizza_type} {flavour}"

    bill_items.append({
        "name": pizza_name,
        "details": (
            f"Base: {base}, Cheese: {cheese}, "
            f"Extra Veggies: {veggies}"
        ),
        "quantity": quantity,
        "price": pizza_cost,
        "total": total_pizza_cost
    })

    print(f"\nPizza added! Total: ₹{total_pizza_cost}")

  
    if not ask_yes_no("Would you like to order another pizza? (yes/no): "):
        break
for category, items in menu.items():

    print(f"\n========== {category.upper()} MENU ==========")

    if ask_yes_no(f"Would you like to order {category.lower()}? (yes/no): "):

        while True:

            item_name = get_choice(
                items.keys(),
                "Choose an item (enter number): "
            )

    
            while True:
                quantity = input("Enter quantity: ")

                if quantity.isdigit() and int(quantity) > 0:
                    quantity = int(quantity)
                    break

                print("Please enter a positive whole number.")

            price = items[item_name]
            total = price * quantity

            bill_items.append({
                "name": item_name,
                "details": category,
                "quantity": quantity,
                "price": price,
                "total": total
            })

            print(f"{item_name} added! Total: ₹{total}")

            if not ask_yes_no(
                f"Would you like another item from {category.lower()}? (yes/no): "
            ):
                break

calculate_total = lambda item: item["total"]

subtotal = sum(map(calculate_total, bill_items))

if subtotal >= 1000:
    discount = subtotal * 0.10
else:
    discount = 0

final_total = subtotal - discount


print("\n")
print("=" * 55)
print("               PYTHON PIZZA")
print("                  FINAL BILL")
print("=" * 55)

print(f"Customer Name: {customer_name}")
print("-" * 55)

print(f"{'Item':<22}{'Qty':>5}{'Price':>10}{'Total':>12}")
print("-" * 55)

for item in bill_items:
    print(
        f"{item['name']:<22}"
        f"{item['quantity']:>5}"
        f"{item['price']:>10.2f}"
        f"{item['total']:>12.2f}"
    )

    print(f"  Details: {item['details']}")
print("-" * 55)
print(f"{'Subtotal:':<37} ₹{subtotal:>10.2f}")
print(f"{'Discount:':<37} ₹{discount:>10.2f}")
print("-" * 55)
print(f"{'FINAL AMOUNT:':<37} ₹{final_total:>10.2f}")
print("=" * 55)
print("\nThank you for visiting Python Pizza!")
print("Enjoy your delicious meal! 🍕")

