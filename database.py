from pymongo import MongoClient


class ConnectionModel:
    @staticmethod
    def connect(collection_name):
        connection_url = MongoClient(host='localhost', port=27017)
        return connection_url['sample'][collection_name]
