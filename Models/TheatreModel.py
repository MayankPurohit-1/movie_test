from database import ConnectionModel
from datetime import datetime
from bson import ObjectId


class TheatreModel:
    def register_theatre(self, theatre_name, num_screens, total_seat):
        result = ConnectionModel.connect('theatre').find_one({"theatre_name": theatre_name}, {"_id": 1})
        if result:
            return {
                "theatre_id": str(result['_id']),
                "msg": "Theatre exists"
            }
        else:
            result = ConnectionModel.connect('theatre').insert_one({
                "theatre_name": theatre_name,
                "num_screen": num_screens,
                "total_seat": total_seat,
                "created_on": datetime.utcnow(),
                "movies": []
            })
            if result.inserted_id:
                return {
                    "msg": "Theatre added",
                    "id": str(result.inserted_id)
                }
            else:
                return {
                    "msg": "something went wrong! failure"
                }

    def register_movie(self, movie_name, screen_num, theatre_id, timing):
        result = ConnectionModel.connect('theatre').find_one({
            "movies.movie_name": movie_name
        })

        print(result)
        if result:
            return {
                "movie_id": str(result['_id']),
                "msg": "Movie exists"
            }
        else:
            result = ConnectionModel.connect('theatre').find_one({"_id": ObjectId(theatre_id)})
            if result:
                if len(result['movies']) < result['num_screen']:
                    data = {
                        "movie_name": movie_name,
                        "screen_num": screen_num,
                        "timing": timing,
                        "added_on": datetime.utcnow()
                    }
                    result = ConnectionModel.connect('theatre').find_one({'_id': ObjectId(theatre_id)})
                    print(result)
                    myquery = {"theatre_name": result['theatre_name']}
                    newquery = {"$push": {"movies": data}}
                    result = ConnectionModel.connect('theatre').update_one(myquery, newquery)
                    if result.modified_count:
                        return {
                            "msg": "Movie added",
                            "id": str(result.modified_count)
                        }
                    else:
                        return {
                            "msg": "something went wrong! failure"
                        }
                else:
                    return {
                        "msg": "Screen Capacity Full"
                    }
            else:
                {
                    "msg": "Theatre Doesn't exists"
                }

    def book_ticket(self, theatre_id, user_id, movie_name, seats, timing):
        ticket_price = 160
        check_movie = ConnectionModel.connect('theatre').find_one({'_id': ObjectId(theatre_id)}, {"movies.movie_name": 1, "_id":0, "total_seat":1})
        print(check_movie)
        for x in check_movie['movies']:
            movie_check = x['movie_name']
        if check_movie:
            if movie_check == movie_name:
                for z in seats:
                    if z > check_movie['total_seat']:
                        return {
                            "msg": "Select correct seats"
                        }
                result = ConnectionModel.connect('basket').find_one({
                    "process_seats": seats,
                    "timing": timing,
                    "movie_name": movie_name
                })
                check_booked = ConnectionModel.connect('payment').find_one({"booked_seats": seats})
                if check_booked:
                    return {
                        "msg": "Ticket already booked"
                    }
                if result:
                    return {
                        "msg": "Ticket booked by someone"
                    }
                else:
                    ConnectionModel.connect('basket').create_index("created_on", expireAfterSeconds=30)
                    result = ConnectionModel.connect('basket').insert_one({
                        "user_id": ObjectId(user_id),
                        "theatre_id": ObjectId(theatre_id),
                        "movie_name": movie_name,
                        "process_seats": seats,
                        "timing": timing,
                        "created_on": datetime.utcnow()
                    })
                    if result.inserted_id:
                        return {
                            "msg": "Ticket basket generated",
                            "id": str(result.inserted_id),
                            "amount_payable": len(seats) * ticket_price
                        }
                    else:
                        return {
                            "msg": 'something went wrong! failure'
                        }
            else:
                return {
                    "msg": "select appropriate movie"
                }
        else:
            return {
                "msg": "This movie is not available"
            }

    def payment(self, basket_id, amount):
        result = ConnectionModel.connect('basket').find_one({"_id": ObjectId(basket_id)})
        if result:
            query = ConnectionModel.connect('payment').find_one({"booked_seats": result['process_seats']})
            if query:
                return {
                    "msg": "Tickets Already booked",
                    "booking_id": str(query['_id'])
                }
            else:
                query = ConnectionModel.connect('payment').insert_one({
                    "user_id": result['user_id'],
                    "theatre_id": result['theatre_id'],
                    "booked_seats": result['process_seats'],
                    "amount paid": amount,
                    "payment_time": datetime.utcnow()
                })
                temp = ConnectionModel.connect('basket').insert_one({
                    "user_id": result['user_id'],
                    "theatre_id": result['theatre_id'],
                    "booked_seats": result['process_seats'],
                    "created_on": datetime.utcnow()
                })
                if query.inserted_id:
                    return {
                        "msg": "Payment Successful",
                        "payment id": str(query.inserted_id)
                    }
                else:
                    return {
                        "msg": "Payment Failed"
                    }
        else:
            return {
                "msg": "Process Timeout"
            }

    def check_seat(self, theatre_id, movie_name, timing):
        result = ConnectionModel.connect('theatre').find_one({
            "_id": ObjectId(theatre_id),
            "movies.movie_name": movie_name,
            "movies.timing": timing
        })
        if result:
            seat_per_screen = result['total_seat'] // result['num_screen']
            print("Seats {}".format(seat_per_screen))
            process_seats = set()
            booked_seats = set()
            query_basket = ConnectionModel.connect('basket').find({'theatre_id': ObjectId(theatre_id)})
            if query_basket:
                for x in query_basket:
                    try:
                        for loop in x['process_seats']:
                            process_seats.add(loop)
                    except KeyError:
                        process_seats = set()

            query_payment = ConnectionModel.connect('payment').find({'theatre_id': ObjectId(theatre_id)})
            if query_payment:
                for x in query_payment:
                    for loop in x['booked_seats']:
                        booked_seats.add(loop)

            if process_seats and booked_seats is None:
                available_seats = seat_per_screen
                return {
                    "available_seats": available_seats
                }
            else:
                total_seats = {s + 1 for s in range(seat_per_screen)}
                print(process_seats)
                print(booked_seats)
                unavailable_seats = process_seats | booked_seats
                available_seats = total_seats - unavailable_seats
                print("Available_seats {}".format(available_seats))
                print("UnAvailable_seats {}".format(unavailable_seats))
                print("Called")
                return {
                    "available_seats": list(available_seats),
                    "process_seats": list(process_seats),
                    "booked_seats": list(booked_seats)
                }
        else:
            return {
                "msg": "CHeck theatre details and try again"
            }
