from flask import Flask
from flask_cors import CORS
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import Config
from src.api.routes import api_bp

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    app.register_blueprint(api_bp)
    
    @app.errorhandler(404)
    def not_found_error(error):
        return {
            'error': 'Not found',
            'message': 'The requested resource was not found.',
            'available_endpoints': [
                '/',
                '/episodes',
                '/episodes/<id>',
                '/episodes/filter',
                '/colors',
                '/subjects',
                '/health',
                '/stats'
            ]
        }, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {
            'error': 'Internal server error',
            'message': 'An unexpected error occurred. Please try again later.'
        }, 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("🎨 Joy of Painting API Starting...")
    print("📋 Available endpoints:")
    print("   GET  /                    - API documentation")
    print("   GET  /episodes            - Get all episodes")
    print("   GET  /episodes/<id>       - Get specific episode")
    print("   GET  /episodes/filter     - Filter episodes")
    print("   POST /episodes/filter     - Filter episodes (JSON)")
    print("   GET  /colors              - Get all colors")
    print("   GET  /subjects            - Get all subjects")
    print("   GET  /health              - Health check")
    print("   GET  /stats               - Database statistics")
    print("")
    print("🌐 API will be available at: http://localhost:5000")
    print("📖 Documentation at: http://localhost:5000")
    print("")
    
    app.run(
        debug=Config.DEBUG,
        host='0.0.0.0',
        port=5000
    )
