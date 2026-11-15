from django.shortcuts import render


def home(request):

    context = {
        "pizza_prices": {
            "Small": {"Veg": 149, "Non-Veg": 199},
            "Medium": {"Veg": 249, "Non-Veg": 299},
            "Large": {"Veg": 349, "Non-Veg": 399}
        },

        "pizza_flavours": {
            "Veg": [
                "Margherita",
                "Farmhouse",
                "Veggie Delight"
            ],

            "Non-Veg": [
                "Chicken Tikka",
                "Pepperoni",
                "BBQ Chicken"
            ]
        },

        "base_prices": {
            "Classic": 0,
            "Thin Crust": 30,
            "Cheese Burst": 60
        },

        "topping_prices": {
            "Extra Cheese": 40,
            "Extra Veggies": 30
        },

        "menu": {
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
    }

    return render(request, "index.html", context) 
