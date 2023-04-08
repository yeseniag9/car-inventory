from flask import Blueprint, request, jsonify, render_template 
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema 

api = Blueprint('api', __name__, url_prefix='/api') 

@api.route('/car', methods = ['POST']) 
@token_required 
def create_car(current_user_token):
    make = request.json['make'] 
    model = request.json['model']
    year = request.json['year']
    price = request.json['price']
    mileage = request.json['mileage']
    color = request.json['color']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(make, model, year, price, mileage, color, user_token = user_token)

    db.session.add(car)
    db.session.commit() 

    response = car_schema.dump(car)
    return jsonify(response) 

@api.route('/cars', methods = ['GET'])
@token_required
def get_car(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id): 
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['POST', 'PUT']) 
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.price = request.json['price']
    car.mileage = request.json['mileage']
    car.color = request.json['color']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)