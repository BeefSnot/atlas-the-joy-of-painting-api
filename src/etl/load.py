import logging
import sys
import os
from typing import Dict, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.models import Episode, Color, Subject
from src.etl.extract import DataExtractor
from src.etl.transform import DataTransformer

logger = logging.getLogger(__name__)

class DataLoader:
    """Load transformed data into MongoDB"""
    
    def __init__(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
    
    def load_colors(self, colors_data: List[Dict]) -> bool:
        """Load colors into database"""
        try:
            Color.delete_all()
            
            if not colors_data:
                logger.warning("No color data to load")
                return True
            
            Color.insert_many(colors_data)
            logger.info(f"Loaded {len(colors_data)} colors")
            return True
            
        except Exception as e:
            logger.error(f"Error loading colors: {e}")
            return False
    
    def load_subjects(self, subjects_data: List[Dict]) -> bool:
        """Load subjects into database"""
        try:
            Subject.delete_all()
            
            if not subjects_data:
                logger.warning("No subject data to load")
                return True
            
            Subject.insert_many(subjects_data)
            logger.info(f"Loaded {len(subjects_data)} subjects")
            return True
            
        except Exception as e:
            logger.error(f"Error loading subjects: {e}")
            return False
    
    def load_episodes(self, episodes_data: List[Dict]) -> bool:
        """Load episodes into database"""
        try:
            Episode.delete_all()
            
            if not episodes_data:
                logger.warning("No episode data to load")
                return True
            
            Episode.insert_many(episodes_data)
            logger.info(f"Loaded {len(episodes_data)} episodes")
            return True
            
        except Exception as e:
            logger.error(f"Error loading episodes: {e}")
            return False
    
    def run_full_etl(self) -> bool:
        """Run complete ETL process"""
        try:
            logger.info("=== Starting Full ETL Process ===")
            
            logger.info("Step 1: Extracting data...")
            raw_data = self.extractor.extract_all()
            
            if not raw_data['episode_dates']:
                logger.error("No episode data extracted. ETL aborted.")
                return False
            
            logger.info("Step 2: Transforming data...")
            transformed_data = self.transformer.transform_all(raw_data)
            
            logger.info("Step 3: Loading data into MongoDB...")
            
            colors_success = self.load_colors(transformed_data['colors'])
            subjects_success = self.load_subjects(transformed_data['subjects'])
            episodes_success = self.load_episodes(transformed_data['episodes'])
            
            if colors_success and subjects_success and episodes_success:
                logger.info("=== ETL Process Completed Successfully ===")
                logger.info(f"Loaded:")
                logger.info(f"  - {len(transformed_data['episodes'])} episodes")
                logger.info(f"  - {len(transformed_data['colors'])} colors")
                logger.info(f"  - {len(transformed_data['subjects'])} subjects")
                return True
            else:
                logger.error("=== ETL Process Failed ===")
                return False
                
        except Exception as e:
            logger.error(f"ETL process failed with error: {e}")
            return False
    
    def verify_data_integrity(self) -> Dict[str, int]:
        """Verify data was loaded correctly"""
        try:
            episodes = Episode.find_all()
            colors = Color.find_all()
            subjects = Subject.find_all()
            
            stats = {
                'episodes': len(episodes),
                'colors': len(colors),
                'subjects': len(subjects)
            }
            
            logger.info(f"Data verification: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error verifying data integrity: {e}")
            return {'episodes': 0, 'colors': 0, 'subjects': 0}

def main():
    """Main ETL function"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    loader = DataLoader()
    
    success = loader.run_full_etl()
    
    if success:
        stats = loader.verify_data_integrity()
        
        if stats['episodes'] > 0:
            print("\n✅ ETL Process Completed Successfully!")
            print(f"📊 Data Summary:")
            print(f"   Episodes: {stats['episodes']}")
            print(f"   Colors: {stats['colors']}")
            print(f"   Subjects: {stats['subjects']}")
            print(f"\n🚀 You can now start the API with: python app.py")
        else:
            print("\n❌ ETL completed but no data was loaded. Please check the logs.")
    else:
        print("\n❌ ETL Process Failed. Please check the logs above.")

if __name__ == "__main__":
    main()
