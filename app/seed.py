#!/usr/bin/env python3

from random import randint, choice as rc

from faker import Faker

from app import app
# from models import db, Bakery, BakedGood
from models import db, Restaurant, Pizza, RestaurantPizza

fake = Faker()

with app.app_context():

    # BakedGood.query.delete()
    # Bakery.query.delete()
    Restaurant.query.delete()
    Pizza.query.delete()
    RestaurantPizza.query.delete()

    restaurants = []
    for i in range(20):
        r = Restaurant(
            name=fake.company(),
            address=fake.address()
        )
        restaurants.append(r)

    db.session.add_all(restaurants)
    db.session.commit()


    pizzas = []
    names = []
    for i in range(100):
        name = fake.first_name()
        while name in names:
            name = fake.first_name()
        names.append(name)

        p = Pizza(
            name=name,
            description=fake.text(),
            price=randint(9,15)
        )
        pizzas.append(p)

    db.session.add_all(pizzas)
    db.session.commit()


    restaurant_pizzas = []
    for i in range(100):
        rp = RestaurantPizza(
            restaurant=rc(restaurants),
            pizza=rc(pizzas),
            price=randint(9,15)
        )
        restaurant_pizzas.append(rp)
    
    db.session.add_all(restaurant_pizzas)
    db.session.commit()

