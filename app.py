from flask import Flask
from flask_restful import Api
from Resource.User import RegisterUser
from Resource.Theatre import RegisterTheatre, RegisterMovie, BookTicket, Payment, CheckSeats

app = Flask(__name__)
api = Api(app)

api.add_resource(RegisterUser, '/register')
api.add_resource(RegisterTheatre, '/addtheatre')
api.add_resource(RegisterMovie, '/addmovie/<string:theatre_id>')
api.add_resource(BookTicket, '/<string:theatre_id>/<string:user_id>/book')
api.add_resource(Payment,'/<string:basket_id>/pay')
api.add_resource(CheckSeats, '/checkseats/<string:theatre_id>/')

app.run(debug=True)
