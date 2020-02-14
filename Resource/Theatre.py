from flask_restful import Resource
from flask import request
from Models.TheatreModel import TheatreModel


class RegisterTheatre(Resource):
    def get(self):
        return "Enter Theatre details"

    def post(self):
        data = request.get_json()
        theatre = TheatreModel()
        return theatre.register_theatre(data['theatre_name'], data['num_screens'], data['total_seats'])


class RegisterMovie(Resource):
    def get(self, theatre_id):
        return "Enter Movie detail to add" + " " + theatre_id

    def post(self, theatre_id):
        data = request.get_json()
        theatre = TheatreModel()
        return theatre.register_movie(data['movie_name'], data['screen_num'], theatre_id, data['timing'])


class BookTicket(Resource):
    def get(self, theatre_id, user_id):
        return {
            "msg": "Enter the detail to book movie"
        }

    def post(self, theatre_id, user_id):
        data = request.get_json()
        ticket = TheatreModel()
        return ticket.book_ticket(theatre_id, user_id, data['movie_name'], data['seats'], data['timing'])


class Payment(Resource):
    def post(self, basket_id):
        data = request.get_json()
        pay = TheatreModel()
        return pay.payment(basket_id, data['amount_payable'])


class CheckSeats(Resource):
    def get(self, theatre_id):
        data = request.get_json()
        check = TheatreModel()
        return check.check_seat(theatre_id, data['movie_name'], data['timing'])



