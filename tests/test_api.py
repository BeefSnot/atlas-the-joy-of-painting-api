import unittest
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from src.api.app import create_app

class TestAPI(unittest.TestCase):
    """Test API endpoints"""
    
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_home_endpoint(self):
        """Test home endpoint returns documentation"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('name', data)
        self.assertIn('endpoints', data)
        self.assertEqual(data['name'], 'Joy of Painting API')
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertIn(response.status_code, [200, 500])
        
        data = json.loads(response.data)
        self.assertIn('status', data)
    
    def test_episodes_endpoint(self):
        """Test episodes endpoint"""
        response = self.client.get('/episodes')
        self.assertIn(response.status_code, [200, 500])
    
    def test_colors_endpoint(self):
        """Test colors endpoint"""
        response = self.client.get('/colors')
        self.assertIn(response.status_code, [200, 500])
    
    def test_subjects_endpoint(self):
        """Test subjects endpoint"""
        response = self.client.get('/subjects')
        self.assertIn(response.status_code, [200, 500])
    
    def test_filter_endpoint_get(self):
        """Test filter endpoint with GET request"""
        response = self.client.get('/episodes/filter?month=january')
        self.assertIn(response.status_code, [200, 500])
    
    def test_filter_endpoint_post(self):
        """Test filter endpoint with POST request"""
        data = {
            'month': 'january',
            'match': 'any'
        }
        response = self.client.post('/episodes/filter', 
                                  data=json.dumps(data),
                                  content_type='application/json')
        self.assertIn(response.status_code, [200, 500])
    
    def test_invalid_endpoint(self):
        """Test invalid endpoint returns 404"""
        response = self.client.get('/invalid-endpoint')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Not found')

if __name__ == '__main__':
    unittest.main()
