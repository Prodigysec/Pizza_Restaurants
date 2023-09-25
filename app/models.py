from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

# Metadata configuration
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# SQLAlchemy configuration
db = SQLAlchemy(metadata=metadata)

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    serialize_rules = ('-restaurant.pizzas', '-pizza.restaurants',) # relationship.related_model

    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    restaurant = db.relationship('Restaurant', back_populates='restaurantPizza')
    pizza = db.relationship('Pizza', back_populates='restaurantPizza')

    @validates("price")
    def validates_price(self, key, price):
        if price < 1 or price > 30:
            raise ValueError("Price must be between 1 and 30!")
        else:
            return price



class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'

    serialize_rules = ('-restaurantPizza.pizza', '-pizzas.restaurants',) # relationship.related_model

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    address = db.Column(db.String)

    pizzas = db.relationship('Pizza', secondary='restaurant_pizzas', back_populates='restaurants')
    restaurantPizza = db.relationship('RestaurantPizza', back_populates='restaurant')

    @validates("name")
    def validates_name(self, key, name):
        if len(name) > 49:
            raise ValueError("Name must be less than 50 character")





class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    serialize_rules = ('-restaurants.pizzas', '-restaurantPizza.restaurant',) # relationship.related_model

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    price = db.Column(db.Integer)

    restaurants = db.relationship('Restaurant', secondary='restaurant_pizzas', back_populates='pizzas')
    restaurantPizza = db.relationship('RestaurantPizza', back_populates='pizza')

    
