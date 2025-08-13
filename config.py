import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

class Config:
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb+srv://jameshamby:Babybluered1@cluster0.eqictx2.mongodb.net/joy_of_painting?retryWrites=true&w=majority'
    
    _parsed_uri = urlparse(MONGODB_URI)
    DATABASE_NAME = _parsed_uri.path.lstrip('/') or 'joy_of_painting'
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    API_PORT = int(os.environ.get('API_PORT', 5000))
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
    
    EPISODE_DATES_FILE = os.path.join(RAW_DATA_DIR, 'episodes.txt')
    COLORS_USED_FILE = os.path.join(RAW_DATA_DIR, 'colors.csv')
    SUBJECT_MATTER_FILE = os.path.join(RAW_DATA_DIR, 'subjects.csv')

if __name__ == "__main__":
    print("🔍 Config Debug:")
    print(f"MONGODB_URI: {Config.MONGODB_URI}")
    print(f"DATABASE_NAME: {Config.DATABASE_NAME}")
    print(f"DATA_DIR: {Config.DATA_DIR}")
