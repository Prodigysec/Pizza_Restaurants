#!/usr/bin/env python3

# Imports
from flask import Flask, make_response, jsonify
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

