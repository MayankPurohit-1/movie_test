from database import ConnectionModel
from datetime import datetime


class UserModel:
    def register_user(self, email, password):
        result = ConnectionModel.connect('user').count({"email": email})
        if result:
            return {
                "msg": "user already exists"
            }
        else:
            result = ConnectionModel.connect('user').insert_one({
                "email": email,
                "password": password,
                "created_on": datetime.utcnow()
            })

            if result.inserted_id:
                return {
                    "id": str(result.inserted_id)
                }
            else:
                return{
                    "msg": "db failed"
                }