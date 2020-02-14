from flask_restful import Resource
from flask import request
from Models.UserModel import UserModel


class RegisterUser(Resource):
    def get(self):
        return "enter user detail"

    def post(self):
         data = request.get_json()
         user = UserModel()
         return user.register_user(data['email'], data['password'])







