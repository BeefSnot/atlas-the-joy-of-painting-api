from bson import ObjectId
from typing import List, Dict, Optional, Any
import logging
from .connection import get_collection

logger = logging.getLogger(__name__)

class Episode:
    """Episode model for MongoDB operations"""
    
    collection_name = 'episodes'
    
    @classmethod
    def get_collection(cls):
        return get_collection(cls.collection_name)
    
    @classmethod
    def find_all(cls, limit: Optional[int] = None, skip: Optional[int] = None) -> List[Dict]:
        """Get all episodes"""
        try:
            collection = cls.get_collection()
            cursor = collection.find()
            
            if skip:
                cursor = cursor.skip(skip)
            if limit:
                cursor = cursor.limit(limit)
                
            episodes = list(cursor)
            
            for episode in episodes:
                episode['_id'] = str(episode['_id'])
            
            return episodes
        except Exception as e:
            logger.error(f"Error finding all episodes: {e}")
            return []
    
    @classmethod
    def find_by_id(cls, episode_id: str) -> Optional[Dict]:
        """Get episode by ID"""
        try:
            collection = cls.get_collection()
            
            try:
                object_id = ObjectId(episode_id)
                episode = collection.find_one({'_id': object_id})
            except:
                episode = collection.find_one({
                    '$or': [
                        {'episode_num': int(episode_id)},
                        {'painting_index': int(episode_id)}
                    ]
                })
            
            if episode:
                episode['_id'] = str(episode['_id'])
            
            return episode
        except Exception as e:
            logger.error(f"Error finding episode by ID {episode_id}: {e}")
            return None
    
    @classmethod
    def filter_episodes(cls, filters: Dict[str, Any], match_type: str = 'any') -> List[Dict]:
        """Filter episodes based on criteria"""
        try:
            collection = cls.get_collection()
            query = {}
            
            if 'month' in filters and filters['month']:
                query['air_date.month_name'] = {'$regex': f"^{filters['month']}", '$options': 'i'}
            
            if 'subjects' in filters and filters['subjects']:
                subjects = [s.strip() for s in filters['subjects']]
                if match_type == 'all':
                    query['subjects'] = {'$all': subjects}
                else:
                    query['subjects'] = {'$in': subjects}
            
            if 'colors' in filters and filters['colors']:
                colors = [c.strip() for c in filters['colors']]
                if match_type == 'all':
                    query['colors.name'] = {'$all': colors}
                else:
                    query['colors.name'] = {'$in': colors}
            
            episodes = list(collection.find(query))
            
            for episode in episodes:
                episode['_id'] = str(episode['_id'])
            
            return episodes
        except Exception as e:
            logger.error(f"Error filtering episodes: {e}")
            return []
    
    @classmethod
    def insert_one(cls, episode_data: Dict) -> Optional[str]:
        """Insert a single episode"""
        try:
            collection = cls.get_collection()
            result = collection.insert_one(episode_data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error inserting episode: {e}")
            return None
    
    @classmethod
    def insert_many(cls, episodes_data: List[Dict]) -> List[str]:
        """Insert multiple episodes"""
        try:
            collection = cls.get_collection()
            result = collection.insert_many(episodes_data)
            return [str(id) for id in result.inserted_ids]
        except Exception as e:
            logger.error(f"Error inserting episodes: {e}")
            return []
    
    @classmethod
    def delete_all(cls):
        """Delete all episodes"""
        try:
            collection = cls.get_collection()
            result = collection.delete_many({})
            logger.info(f"Deleted {result.deleted_count} episodes")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting episodes: {e}")
            return 0

class Color:
    """Color model for MongoDB operations"""
    
    collection_name = 'colors'
    
    @classmethod
    def get_collection(cls):
        return get_collection(cls.collection_name)
    
    @classmethod
    def find_all(cls) -> List[Dict]:
        """Get all colors"""
        try:
            collection = cls.get_collection()
            colors = list(collection.find())
            
            for color in colors:
                color['_id'] = str(color['_id'])
            
            return colors
        except Exception as e:
            logger.error(f"Error finding all colors: {e}")
            return []
    
    @classmethod
    def insert_many(cls, colors_data: List[Dict]) -> List[str]:
        """Insert multiple colors"""
        try:
            collection = cls.get_collection()
            result = collection.insert_many(colors_data)
            return [str(id) for id in result.inserted_ids]
        except Exception as e:
            logger.error(f"Error inserting colors: {e}")
            return []
    
    @classmethod
    def delete_all(cls):
        """Delete all colors"""
        try:
            collection = cls.get_collection()
            result = collection.delete_many({})
            logger.info(f"Deleted {result.deleted_count} colors")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting colors: {e}")
            return 0

class Subject:
    """Subject model for MongoDB operations"""
    
    collection_name = 'subjects'
    
    @classmethod
    def get_collection(cls):
        return get_collection(cls.collection_name)
    
    @classmethod
    def find_all(cls) -> List[Dict]:
        """Get all subjects"""
        try:
            collection = cls.get_collection()
            subjects = list(collection.find())
            
            for subject in subjects:
                subject['_id'] = str(subject['_id'])
            
            return subjects
        except Exception as e:
            logger.error(f"Error finding all subjects: {e}")
            return []
    
    @classmethod
    def insert_many(cls, subjects_data: List[Dict]) -> List[str]:
        """Insert multiple subjects"""
        try:
            collection = cls.get_collection()
            result = collection.insert_many(subjects_data)
            return [str(id) for id in result.inserted_ids]
        except Exception as e:
            logger.error(f"Error inserting subjects: {e}")
            return []
    
    @classmethod
    def delete_all(cls):
        """Delete all subjects"""
        try:
            collection = cls.get_collection()
            result = collection.delete_many({})
            logger.info(f"Deleted {result.deleted_count} subjects")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting subjects: {e}")
            return 0
