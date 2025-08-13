import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import Config
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """MongoDB database connection manager"""
    
    def __init__(self):
        self._client = None
        self._db = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            parsed_uri = urlparse(Config.MONGODB_URI)
            db_name = parsed_uri.path.lstrip('/') if parsed_uri.path else 'joy_of_painting'
            
            if '?' in db_name:
                db_name = db_name.split('?')[0]
            
            logger.info(f"Connecting to MongoDB at: {parsed_uri.netloc}")
            logger.info(f"Database name: {db_name}")
            
            self._client = MongoClient(Config.MONGODB_URI)
            
            self._client.admin.command('ping')
            logger.info("✅ MongoDB connection successful")
            
            self._db = self._client[db_name]
            logger.info(f"✅ Connected to database: {db_name}")
            
        except ConnectionFailure as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected error connecting to MongoDB: {e}")
            raise
    
    def get_database(self):
        """Get database instance"""
        if self._db is None:
            self.connect()
        return self._db
    
    def get_client(self):
        """Get client instance"""
        if self._client is None:
            self.connect()
        return self._client
    
    def close(self):
        """Close database connection"""
        if self._client:
            self._client.close()
            logger.info("🔌 MongoDB connection closed")

_db_connection = None

def get_database():
    """Get database instance"""
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection()
    return _db_connection.get_database()

def get_client():
    """Get client instance"""
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection()
    return _db_connection.get_client()

def get_collection(collection_name):
    """Get collection from database"""
    db = get_database()
    return db[collection_name]

def close_connection():
    """Close database connection"""
    global _db_connection
    if _db_connection:
        _db_connection.close()
        _db_connection = None
