import re
import logging
from datetime import datetime
from typing import List, Dict, Any
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

logger = logging.getLogger(__name__)

class DataTransformer:
    """Transform extracted data for database storage"""
    
    def __init__(self):
        self.month_mapping = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }
    
    def parse_air_date(self, date_str: str) -> Dict[str, Any]:
        """Parse air date string to structured date info"""
        try:
            date_str = date_str.strip()
            
            try:
                date_obj = datetime.strptime(date_str, "%B %d, %Y")
            except ValueError:
                try:
                    date_obj = datetime.strptime(date_str, "%B %d %Y")
                except ValueError:
                    logger.warning(f"Could not parse date: {date_str}")
                    date_obj = datetime(1983, 1, 1)
            
            return {
                'date': date_obj,
                'year': date_obj.year,
                'month': date_obj.month,
                'day': date_obj.day,
                'month_name': date_obj.strftime("%B").lower(),
                'formatted': date_obj.strftime("%Y-%m-%d")
            }
            
        except Exception as e:
            logger.warning(f"Error parsing date '{date_str}': {e}")
            default_date = datetime(1983, 1, 1)
            return {
                'date': default_date,
                'year': 1983,
                'month': 1,
                'day': 1,
                'month_name': 'january',
                'formatted': '1983-01-01'
            }
    
    def clean_title(self, title: str) -> str:
        """Clean episode title"""
        if not title:
            return ""
        
        title = title.strip().strip('"').strip()
        
        title = title.title()
        
        return title
    
    def normalize_color_name(self, color_name: str) -> str:
        """Normalize color names"""
        if not color_name:
            return ""
        
        color_name = color_name.strip().replace('\r\n', '').replace('\n', '')
        
        color_name = color_name.title()
        
        return color_name
    
    def normalize_subject_name(self, subject_name: str) -> str:
        """Normalize subject names"""
        if not subject_name:
            return ""
        
        subject_name = subject_name.strip()
        
        replacements = {
            'Mt.': 'Mount',
            'Mt ': 'Mount ',
            'Steve Ross': 'Steve Ross',
            'Diane Andre': 'Diane Andre'
        }
        
        for old, new in replacements.items():
            subject_name = subject_name.replace(old, new)
        
        return subject_name
    
    def merge_episode_data(self, episode_dates: List[Dict], colors_data: List[Dict], 
                          subject_data: List[Dict]) -> List[Dict]:
        """Merge all episode data into unified structure"""
        
        colors_lookup = {item['episode_num']: item for item in colors_data}
        subjects_lookup = {item['episode_num']: item for item in subject_data}
        
        merged_episodes = []
        
        for episode_date in episode_dates:
            episode_num = episode_date['episode_num']
            
            color_info = colors_lookup.get(episode_num, {})
            subject_info = subjects_lookup.get(episode_num, {})
            
            air_date_info = self.parse_air_date(episode_date['air_date_str'])
            
            title = self.clean_title(
                color_info.get('title') or episode_date.get('title', '')
            )
            
            colors = []
            unique_color_names = set()
            
            for color in color_info.get('colors', []):
                color_name = self.normalize_color_name(color.get('name', ''))
                if color_name and color_name not in unique_color_names:
                    colors.append({
                        'name': color_name,
                        'hex': color.get('hex')
                    })
                    unique_color_names.add(color_name)
            
            subjects = []
            for subject in subject_info.get('subjects', []):
                subject_name = self.normalize_subject_name(subject)
                if subject_name:
                    subjects.append(subject_name)
            
            merged_episode = {
                'episode_num': episode_num,
                'painting_index': color_info.get('painting_index', episode_num),
                'title': title,
                'season': episode_date['season'],
                'episode': episode_date['episode'],
                'air_date': air_date_info,
                'colors': colors,
                'subjects': subjects,
                'youtube_url': color_info.get('youtube_src', ''),
                'img_src': color_info.get('img_src', ''),
                'num_colors': len(colors),
                'num_subjects': len(subjects)
            }
            
            merged_episodes.append(merged_episode)
        
        logger.info(f"Merged {len(merged_episodes)} episodes")
        return merged_episodes
    
    def extract_unique_colors(self, episodes: List[Dict]) -> List[Dict]:
        """Extract unique colors from all episodes"""
        colors_dict = {}
        
        for episode in episodes:
            for color in episode.get('colors', []):
                color_name = color['name']
                if color_name not in colors_dict:
                    colors_dict[color_name] = {
                        'name': color_name,
                        'hex': color.get('hex'),
                        'episodes': []
                    }
                colors_dict[color_name]['episodes'].append(episode['episode_num'])
        
        unique_colors = []
        for color_name, color_data in colors_dict.items():
            unique_colors.append({
                'name': color_name,
                'hex': color_data['hex'],
                'episode_count': len(color_data['episodes']),
                'episodes': color_data['episodes']
            })
        
        unique_colors.sort(key=lambda x: x['episode_count'], reverse=True)
        
        logger.info(f"Found {len(unique_colors)} unique colors")
        return unique_colors
    
    def extract_unique_subjects(self, episodes: List[Dict]) -> List[Dict]:
        """Extract unique subjects from all episodes"""
        subjects_dict = {}
        
        for episode in episodes:
            for subject in episode.get('subjects', []):
                if subject not in subjects_dict:
                    subjects_dict[subject] = {
                        'name': subject,
                        'episodes': []
                    }
                subjects_dict[subject]['episodes'].append(episode['episode_num'])
        
        unique_subjects = []
        for subject_name, subject_data in subjects_dict.items():
            unique_subjects.append({
                'name': subject_name,
                'episode_count': len(subject_data['episodes']),
                'episodes': subject_data['episodes']
            })
        
        unique_subjects.sort(key=lambda x: x['episode_count'], reverse=True)
        
        logger.info(f"Found {len(unique_subjects)} unique subjects")
        return unique_subjects
    
    def transform_all(self, raw_data: Dict) -> Dict:
        """Transform all extracted data"""
        logger.info("Starting data transformation...")
        
        episodes = self.merge_episode_data(
            raw_data['episode_dates'],
            raw_data['colors_data'],
            raw_data['subject_data']
        )
        
        colors = self.extract_unique_colors(episodes)
        subjects = self.extract_unique_subjects(episodes)
        
        return {
            'episodes': episodes,
            'colors': colors,
            'subjects': subjects
        }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    from extract import DataExtractor
    
    extractor = DataExtractor()
    raw_data = extractor.extract_all()
    
    transformer = DataTransformer()
    transformed_data = transformer.transform_all(raw_data)
    
    print(f"Transformed:")
    print(f"- {len(transformed_data['episodes'])} episodes")
    print(f"- {len(transformed_data['colors'])} unique colors")
    print(f"- {len(transformed_data['subjects'])} unique subjects")
