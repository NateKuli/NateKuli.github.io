import os
import logging
from typing import Any, Dict, List, Optional
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

class AnimalShelter:
    """
    A secure and modular CRUD interface for the AAC MongoDB 'animals' collection.

    This class provides validated and logged CRUD operations while following
    software engineering best practices for CS 499 Milestone Two.
    """

    def __init__(self):
        """
        Initialize the MongoDB client using environment variables.

        Expected environment variables:
            MONGO_USER
            MONGO_PASS
            MONGO_HOST
            MONGO_PORT
            MONGO_DB
            MONGO_COLLECTION
        """
        try:
            username = os.getenv("MONGO_USER")
            password = os.getenv("MONGO_PASS")
            host = os.getenv("MONGO_HOST", "localhost")
            port = os.getenv("MONGO_PORT", "27017")
            db_name = os.getenv("MONGO_DB", "aac")
            col_name = os.getenv("MONGO_COLLECTION", "animals")

            if not username or not password:
                raise ValueError("Missing MongoDB credentials in environment variables.")

            uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}"
            self.client = MongoClient(uri)
            self.database = self.client[db_name]
            self.collection = self.database[col_name]

            logging.info("MongoDB connection established successfully.")

        except Exception as e:
            logging.error(f"Failed to initialize MongoDB connection: {e}")
            raise

    # -----------------------------
    # CREATE
    # -----------------------------
    def create(self, data: Dict[str, Any]) -> bool:
        """
        Insert a document into the collection.

        Args:
            data: A dictionary representing the document to insert.

        Returns:
            True if successful, False otherwise.
        """
        if not isinstance(data, dict) or not data:
            raise ValueError("Data must be a non-empty dictionary.")

        try:
            self.collection.insert_one(data)
            logging.info("Document inserted successfully.")
            return True
        except PyMongoError as e:
            logging.error(f"Insert failed: {e}")
            return False

    # -----------------------------
    # READ
    # -----------------------------
    def read(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Query documents from the collection.

        Args:
            query: A dictionary representing the MongoDB query.

        Returns:
            A list of matching documents.
        """
        if not isinstance(query, dict):
            raise ValueError("Query must be a dictionary.")

        try:
            results = list(self.collection.find(query))
            logging.info(f"Query returned {len(results)} documents.")
            return results
        except PyMongoError as e:
            logging.error(f"Query failed: {e}")
            return []

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update(self, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        """
        Update documents in the collection.

        Args:
            query: A dictionary specifying which documents to update.
            update_data: A dictionary of fields to update.

        Returns:
            The number of modified documents.
        """
        if not isinstance(query, dict) or not isinstance(update_data, dict):
            raise ValueError("Query and update_data must be dictionaries.")

        try:
            result = self.collection.update_many(query, {"$set": update_data})
            logging.info(f"Updated {result.modified_count} documents.")
            return result.modified_count
        except PyMongoError as e:
            logging.error(f"Update failed: {e}")
            return 0

    # -----------------------------
    # DELETE
    # -----------------------------
    def delete(self, query: Dict[str, Any]) -> int:
        """
        Delete documents from the collection.

        Args:
            query: A dictionary specifying which documents to delete.

        Returns:
            The number of deleted documents.
        """
        if not isinstance(query, dict):
            raise ValueError("Query must be a dictionary.")

        try:
            result = self.collection.delete_many(query)
            logging.info(f"Deleted {result.deleted_count} documents.")
            return result.deleted_count
        except PyMongoError as e:
            logging.error(f"Delete failed: {e}")
            return 0

    # -----------------------------
    # READ ALL
    # -----------------------------
    def read_all(self) -> List[Dict[str, Any]]:
        """
        Retrieve all documents from the collection.

        Returns:
            A list of all documents.
        """
        try:
            results = list(self.collection.find({}))
            logging.info(f"Retrieved {len(results)} total documents.")
            return results
        except PyMongoError as e:
            logging.error(f"Read all failed: {e}")
            return []
