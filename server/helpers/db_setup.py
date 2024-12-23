from pymongo import MongoClient, errors

from .config import configData
from .logger_setup import logger

class Database:
    def __init__(self):
        self.connStr = f"mongodb://{configData['database']['host']}:{configData['database']['port']}"
        self.client = MongoClient(self.connStr)
        self.db = self.client[configData["database"]["name"]]

    def getData(self, collection, query={}, projection={}):
        try:
            return list(self.db[collection].find(query, projection))
        except errors.PyMongoError as e:
            logger.error(f"Error in getData: {e}")
            return []

    def insertData(self, collection, data):
        try:
            if isinstance(data, list):
                if not data:
                    raise ValueError("Data list cannot be empty.")
                result = self.db[collection].insert_many(data)
                return result.inserted_ids
            elif isinstance(data, dict): 
                result = self.db[collection].insert_one(data)
                return result.inserted_id
            else:
                raise TypeError("Data must be a dictionary or a list of dictionaries.")
        except (errors.PyMongoError, ValueError, TypeError) as e:
            logger.error(f"Error in insertData: {e}")
            return None

    def upsertData(self, collection, query, data):
        try:
            if not isinstance(data, dict): 
                raise TypeError("Data must be a dictionary.")

            result = self.db[collection].update_one(query, {"$set": data}, upsert=True)
            return result.modified_count, result.upserted_id 
        except (errors.PyMongoError, TypeError) as e:
            logger.error(f"Error in upsertData: {e}")
            return None

    def updateData(self, collection, query, data):
        try:
            if not isinstance(data, dict):
                raise TypeError("Data must be a dictionary.")

            result = self.db[collection].update_many(query, {"$set": data})
            return result.modified_count 
        except (errors.PyMongoError, TypeError) as e:
            logger.error(f"Error in updateData: {e}")
            return None

    def deleteData(self, collection, query={}):
        try:
            result = self.db[collection].delete_many(query)
            return result.deleted_count 
        except errors.PyMongoError as e:
            logger.error(f"Error in deleteData: {e}")
            return None

dbConn = Database()