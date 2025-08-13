from typing import List, Dict, Any, Optional
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.models import Episode, Color, Subject

logger = logging.getLogger(__name__)

class EpisodeFilter:
    """Handle episode filtering logic"""
    
    @staticmethod
    def parse_filter_params(data: Dict) -> Dict[str, Any]:
        """Parse and validate filter parameters"""
        filters = {}
        
        month = data.get('month')
        if month:
            filters['month'] = month.strip().lower()
        
        subjects = data.get('subjects')
        if subjects:
            if isinstance(subjects, str):
                filters['subjects'] = [s.strip() for s in subjects.split(',') if s.strip()]
            elif isinstance(subjects, list):
                filters['subjects'] = [s.strip() for s in subjects if s.strip()]
        
        colors = data.get('colors')
        if colors:
            if isinstance(colors, str):
                filters['colors'] = [c.strip() for c in colors.split(',') if c.strip()]
            elif isinstance(colors, list):
                filters['colors'] = [c.strip() for c in colors if c.strip()]
        
        return filters
    
    @staticmethod
    def filter_episodes(filters: Dict[str, Any], match_type: str = 'any') -> List[Dict]:
        """Filter episodes based on criteria"""
        try:
            episodes = Episode.find_all()
            
            if not filters:
                return episodes
            
            filtered_episodes = []
            
            for episode in episodes:
                include_episode = True
                matches = []
                
                if 'month' in filters:
                    month_match = (
                        episode.get('air_date', {}).get('month_name', '').lower() == 
                        filters['month'].lower()
                    )
                    matches.append(month_match)
                
                if 'subjects' in filters:
                    episode_subjects = [s.lower() for s in episode.get('subjects', [])]
                    filter_subjects = [s.lower() for s in filters['subjects']]
                    
                    if match_type == 'all':
                        subjects_match = all(
                            any(fs in es for es in episode_subjects) 
                            for fs in filter_subjects
                        )
                    else:
                        subjects_match = any(
                            any(fs in es for es in episode_subjects) 
                            for fs in filter_subjects
                        )
                    
                    matches.append(subjects_match)
                
                if 'colors' in filters:
                    episode_colors = [c.get('name', '').lower() for c in episode.get('colors', [])]
                    filter_colors = [c.lower() for c in filters['colors']]
                    
                    if match_type == 'all':
                        colors_match = all(
                            any(fc in ec for ec in episode_colors) 
                            for fc in filter_colors
                        )
                    else:
                        colors_match = any(
                            any(fc in ec for ec in episode_colors) 
                            for fc in filter_colors
                        )
                    
                    matches.append(colors_match)
                
                if match_type == 'all':
                    include_episode = all(matches) if matches else True
                else:
                    include_episode = any(matches) if matches else True
                
                if include_episode:
                    filtered_episodes.append(episode)
            
            logger.info(f"Filtered {len(filtered_episodes)} episodes from {len(episodes)} total")
            return filtered_episodes
            
        except Exception as e:
            logger.error(f"Error filtering episodes: {e}")
            return []

class APIHelpers:
    """Helper functions for API responses"""
    
    @staticmethod
    def format_episode_response(episode: Dict) -> Dict:
        """Format episode for API response"""
        if not episode:
            return None
        
        color_names = [color.get('name') for color in episode.get('colors', [])]
        
        return {
            'id': episode.get('_id'),
            'episode_num': episode.get('episode_num'),
            'painting_index': episode.get('painting_index'),
            'title': episode.get('title'),
            'season': episode.get('season'),
            'episode': episode.get('episode'),
            'air_date': episode.get('air_date', {}),
            'colors': episode.get('colors', []),
            'color_names': color_names,
            'subjects': episode.get('subjects', []),
            'youtube_url': episode.get('youtube_url'),
            'img_src': episode.get('img_src'),
            'num_colors': episode.get('num_colors', 0),
            'num_subjects': episode.get('num_subjects', 0)
        }
    
    @staticmethod
    def format_episodes_response(episodes: List[Dict], filters_applied: Dict = None) -> Dict:
        """Format multiple episodes for API response"""
        formatted_episodes = [
            APIHelpers.format_episode_response(episode) 
            for episode in episodes
        ]
        
        response = {
            'episodes': formatted_episodes,
            'total': len(formatted_episodes)
        }
        
        if filters_applied:
            response['filters_applied'] = filters_applied
        
        return response
    
    @staticmethod
    def get_api_documentation() -> Dict:
        """Get API documentation"""
        return {
            'name': 'Joy of Painting API',
            'version': '1.0.0',
            'description': 'API for filtering Bob Ross episodes by month, subjects, and colors',
            'endpoints': {
                'GET /': 'API documentation',
                'GET /episodes': 'Get all episodes',
                'GET /episodes/<id>': 'Get specific episode by ID',
                'GET /episodes/filter': 'Filter episodes with query parameters',
                'POST /episodes/filter': 'Filter episodes with JSON body',
                'GET /colors': 'Get all available colors',
                'GET /subjects': 'Get all available subjects'
            },
            'filter_parameters': {
                'month': 'Filter by month name (e.g., january, february)',
                'subjects': 'Filter by subjects (comma-separated)',
                'colors': 'Filter by colors (comma-separated)',
                'match': 'Match type: "any" (default) or "all"'
            },
            'examples': {
                'filter_by_month': '/episodes/filter?month=january',
                'filter_by_subjects_any': '/episodes/filter?subjects=mountain,tree&match=any',
                'filter_by_colors_all': '/episodes/filter?colors=Prussian Blue,Titanium White&match=all',
                'combined_filters': '/episodes/filter?month=january&subjects=mountain&colors=blue&match=all'
            }
        }
