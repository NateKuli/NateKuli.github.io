from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId

class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB"""

    def __init__(self, username, password):
        HOST = 'localhost'
        PORT = 27017
        DB = 'aac'
        COL = 'animals'

        try:
            self.client = MongoClient(f'mongodb://{username}:{password}@{HOST}:{PORT}/{DB}')
            self.database = self.client[DB]
            self.collection = self.database[COL]
        except PyMongoError as e:
            print(f"Connection failed: {e}")
            self.collection = None


    def create(self, data):
        """Insert a document into the collection."""
        if data:
            try:
                self.collection.insert_one(data)
                return True
            except PyMongoError as e:
                print(f"Insert failed: {e}")
                return False
        else:
            raise ValueError("Nothing to save, because data parameter is empty")

    def read(self, query):
        """Query documents from the collection."""
        if query:
            try:
                return list(self.collection.find(query))
            except PyMongoError as e:
                print(f"Query failed: {e}")
                return []
        else:
            raise ValueError("Query parameter is empty")

    def update(self, query, update_data):
        """Update documents in the collection."""
        if query and update_data:
            try:
                result = self.collection.update_many(query, {'$set': update_data})
                return result.modified_count
            except PyMongoError as e:
                print(f"Update failed: {e}")
                return 0
        else:
            raise ValueError("Query and update_data parameters must not be empty")

    def delete(self, query):
        """Delete documents from the collection."""
        if query:
            try:
                result = self.collection.delete_many(query)
                return result.deleted_count
            except PyMongoError as e:
                print(f"Delete failed: {e}")
                return 0
        else:
            raise ValueError("Query parameter is empty")
                    
    def read_all(self):
        """Retrieve all documents from the collection."""
        try:
            return list(self.collection.find({}))
        except PyMongoError as e:
            print(f"Read all failed: {e}")
            return []          