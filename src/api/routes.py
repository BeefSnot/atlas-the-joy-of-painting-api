from flask import Blueprint, request, jsonify
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.models import Episode, Color, Subject
from src.api.filters import EpisodeFilter, APIHelpers

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

@api_bp.route('/', methods=['GET'])
def home():
    """API documentation and endpoints"""
    try:
        return jsonify(APIHelpers.get_api_documentation())
    except Exception as e:
        logger.error(f"Error getting documentation: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/episodes', methods=['GET'])
def get_all_episodes():
    """Get all episodes"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        skip = (page - 1) * per_page
        
        episodes = Episode.find_all(limit=per_page, skip=skip)
        
        response = APIHelpers.format_episodes_response(episodes)
        response['page'] = page
        response['per_page'] = per_page
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error getting all episodes: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/episodes/<episode_id>', methods=['GET'])
def get_episode_by_id(episode_id):
    """Get specific episode by ID"""
    try:
        episode = Episode.find_by_id(episode_id)
        
        if not episode:
            return jsonify({'error': 'Episode not found'}), 404
        
        formatted_episode = APIHelpers.format_episode_response(episode)
        return jsonify(formatted_episode)
        
    except Exception as e:
        logger.error(f"Error getting episode {episode_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/episodes/filter', methods=['GET', 'POST'])
def filter_episodes():
    """Filter episodes by criteria"""
    try:
        if request.method == 'POST':
            data = request.get_json() or {}
        else:
            data = request.args.to_dict()
        
        filters = EpisodeFilter.parse_filter_params(data)
        match_type = data.get('match', 'any').lower()
        
        if match_type not in ['any', 'all']:
            return jsonify({'error': 'match parameter must be "any" or "all"'}), 400
        
        episodes = EpisodeFilter.filter_episodes(filters, match_type)
        
        filters_applied = {
            'month': filters.get('month'),
            'subjects': filters.get('subjects'),
            'colors': filters.get('colors'),
            'match_type': match_type
        }
        
        response = APIHelpers.format_episodes_response(episodes, filters_applied)
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error filtering episodes: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/colors', methods=['GET'])
def get_all_colors():
    """Get all available colors"""
    try:
        colors = Color.find_all()
        
        colors.sort(key=lambda x: x.get('name', ''))
        
        return jsonify({
            'colors': colors,
            'total': len(colors)
        })
        
    except Exception as e:
        logger.error(f"Error getting colors: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/subjects', methods=['GET'])
def get_all_subjects():
    """Get all available subjects"""
    try:
        subjects = Subject.find_all()
        
        subjects.sort(key=lambda x: x.get('name', ''))
        
        return jsonify({
            'subjects': subjects,
            'total': len(subjects)
        })
        
    except Exception as e:
        logger.error(f"Error getting subjects: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        Episode.find_all(limit=1)
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        episodes = Episode.find_all()
        colors = Color.find_all()
        subjects = Subject.find_all()
        
        total_episodes = len(episodes)
        total_colors = len(colors)
        total_subjects = len(subjects)
        
        color_usage = {}
        subject_usage = {}
        
        for episode in episodes:
            for color in episode.get('colors', []):
                color_name = color.get('name')
                if color_name:
                    color_usage[color_name] = color_usage.get(color_name, 0) + 1
            
            for subject in episode.get('subjects', []):
                subject_usage[subject] = subject_usage.get(subject, 0) + 1
        
        top_colors = sorted(color_usage.items(), key=lambda x: x[1], reverse=True)[:10]
        top_subjects = sorted(subject_usage.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return jsonify({
            'total_episodes': total_episodes,
            'total_colors': total_colors,
            'total_subjects': total_subjects,
            'top_colors': [{'name': name, 'count': count} for name, count in top_colors],
            'top_subjects': [{'name': name, 'count': count} for name, count in top_subjects]
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': 'Internal server error'}), 500
