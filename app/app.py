#!/usr/bin/env python3

# Imports
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate

# from models import
from models import db, Restaurant, Pizza, RestaurantPizza

# Create Flask app instance
app = Flask(__name__)

# DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JSON config
app.json.compact = False

# DB migration manager
migrate = Migrate(app, db)

# DB init
db.init_app(app)

# Routes
@app.route('/')
def index():
    return '<h1>Pizza Restaurants</h1>'


@app.route('/restaurants')
def restaurants():
    restaurants = []
    for restaurant in Restaurant.query.all():
        restaurant_dict = {
            "name": restaurant.name,
            "address": restaurant.address,
        }
        restaurants.append(restaurant_dict)

    response = make_response(
        jsonify(restaurants),
        200
    )

    return response


@app.route('/restaurants/<int:restaurant_id>')
def restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return make_response(
            jsonify({"error": "Not found"}),
            404
        )
    else:
        restaurant_dict = {
        "name": restaurant.name,
        "address": restaurant.address,
    }

    response = make_response(
        jsonify(restaurant_dict),
        200
    )

    return response


@app.route('/restaurants/<int:restaurant_id>', methods=['GET','DELETE'])
def restaurant_by_id(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return make_response(
            jsonify({"error": "Not found"}),
            404
        )
    else:
        if request.method == 'DELETE':
            try:
                restaurant_pizzas = RestaurantPizza.query.filter_by(restaurant_id=restaurant_id).delete()
                db.session.delete(restaurant)
                db.session.commit()

                response_body = {
                    "message": "Restaurant deleted."
                }
                response = make_response(
                    jsonify(response_body),
                    204
                )
                return response
            except:
                db.session.rollback()
                return make_response(
                    jsonify({'message': 'Error occured while deleting database'})
                )



@app.route('/pizzas')
def pizzas():
    pizzas = []
    for pizza in Pizza.query.all():
        pizza_dict = {
            "name": pizza.name,
            "description": pizza.description,
            "price": pizza.price,
        }
        pizzas.append(pizza_dict)

    response = make_response(
        jsonify(pizzas),
        200
    )

    return response


@app.route('/restaurantpizza', methods = ['POST'])
def create_RestaurantPizza():
    if request.method == 'POST':

        data = request.get_json()
        restaurant_id = data.get('restaurant_id')
        pizza_id = data.get('pizza_id')
        price = data.get('price')


        restaurant = Restaurant.query.get(restaurant_id)
        pizza = Pizza.query.get(pizza_id)

        if not restaurant or not pizza:
            return jsonify({'error': 'Restaurant or pizza not found'}), 404
        
        else:
            try:
                restaurantPizza = RestaurantPizza(
                    pizza_id=pizza_id,
                    restaurant_id=restaurant_id,
                    price=int(price)
                )
                db.session.add(restaurantPizza)
                db.session.commit()

                response_body = {
                    "message": "RestaurantPizza created."
                }
                return make_response(
                    jsonify(response_body),
                    201
                )
            except:
                db.session.rollback()
                return make_response(
                    jsonify({'message': 'Error occured while creating database'})
                )
    

# Main block
if __name__ == '__main__':
    app.run(port=5555, debug=True)