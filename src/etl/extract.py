import pandas as pd
import os
import re
import json
import logging
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import Config

logger = logging.getLogger(__name__)

class DataExtractor:
    """Extract data from raw files"""
    
    def __init__(self):
        self.base_dir = Config.BASE_DIR
    
    def extract_episode_dates(self):
        """Extract episode dates from the episode dates file"""
        try:
            filepath = Config.EPISODE_DATES_FILE
            
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            episodes = []
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line:
                    match = re.match(r'"(.+)"\s*\((.+)\)', line)
                    if match:
                        title = match.group(1)
                        date_str = match.group(2)
                        
                        episodes.append({
                            'episode_num': i,
                            'title': title,
                            'air_date_str': date_str,
                            'season': (i - 1) // 13 + 1,
                            'episode': ((i - 1) % 13) + 1
                        })
            
            logger.info(f"Extracted {len(episodes)} episodes from dates file")
            return episodes
            
        except Exception as e:
            logger.error(f"Error extracting episode dates: {e}")
            return []
    
    def extract_colors_used(self):
        """Extract colors data from CSV file"""
        try:
            filepath = Config.COLORS_USED_FILE
            
            df = pd.read_csv(filepath)
            
            colors_data = []
            for _, row in df.iterrows():
                colors_str = row.get('colors', '[]')
                hex_str = row.get('color_hex', '[]')
                
                try:
                    colors_str = colors_str.replace('\r\n', '').replace("'", '"')
                    hex_str = hex_str.replace("'", '"')
                    
                    colors = json.loads(colors_str) if colors_str != '[]' else []
                    hex_values = json.loads(hex_str) if hex_str != '[]' else []
                    
                    episode_colors = []
                    for i, color in enumerate(colors):
                        color_data = {
                            'name': color.strip(),
                            'hex': hex_values[i] if i < len(hex_values) else None
                        }
                        episode_colors.append(color_data)
                    
                    colors_data.append({
                        'painting_index': int(row.get('painting_index', 0)),
                        'episode_num': int(row.get('painting_index', 0)),
                        'title': row.get('painting_title', ''),
                        'season': int(row.get('season', 1)),
                        'episode': int(row.get('episode', 1)),
                        'img_src': row.get('img_src', ''),
                        'youtube_src': row.get('youtube_src', ''),
                        'colors': episode_colors,
                        'num_colors': len(episode_colors)
                    })
                    
                except json.JSONDecodeError as e:
                    logger.warning(f"Error parsing colors for row {row.get('painting_index')}: {e}")
                    continue
            
            logger.info(f"Extracted {len(colors_data)} episodes with color data")
            return colors_data
            
        except Exception as e:
            logger.error(f"Error extracting colors data: {e}")
            return []
    
    def extract_subject_matter(self):
        """Extract subject matter data from CSV file"""
        try:
            filepath = Config.SUBJECT_MATTER_FILE
            
            df = pd.read_csv(filepath)
            
            subject_data = []
            
            subject_columns = [col for col in df.columns if col not in ['EPISODE', 'TITLE']]
            
            for _, row in df.iterrows():
                episode_code = row['EPISODE']
                title = row['TITLE'].strip('"')
                
                match = re.match(r'S(\d+)E(\d+)', episode_code)
                if match:
                    season = int(match.group(1))
                    episode = int(match.group(2))
                    episode_num = (season - 1) * 13 + episode
                else:
                    continue
                
                subjects = []
                for subject_col in subject_columns:
                    if row[subject_col] == 1:
                        subject_name = subject_col.replace('_', ' ').title()
                        subjects.append(subject_name)
                
                subject_data.append({
                    'episode_num': episode_num,
                    'episode_code': episode_code,
                    'title': title,
                    'season': season,
                    'episode': episode,
                    'subjects': subjects
                })
            
            logger.info(f"Extracted {len(subject_data)} episodes with subject data")
            return subject_data
            
        except Exception as e:
            logger.error(f"Error extracting subject data: {e}")
            return []
    
    def extract_all(self):
        """Extract all data"""
        logger.info("Starting data extraction...")
        
        episode_dates = self.extract_episode_dates()
        colors_data = self.extract_colors_used()
        subject_data = self.extract_subject_matter()
        
        return {
            'episode_dates': episode_dates,
            'colors_data': colors_data,
            'subject_data': subject_data
        }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    extractor = DataExtractor()
    data = extractor.extract_all()
    
    print(f"Extracted:")
    print(f"- {len(data['episode_dates'])} episode dates")
    print(f"- {len(data['colors_data'])} episodes with colors")
    print(f"- {len(data['subject_data'])} episodes with subjects")
