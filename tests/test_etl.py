import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from src.etl.extract import DataExtractor
from src.etl.transform import DataTransformer

class TestETL(unittest.TestCase):
    """Test ETL processes"""
    
    def setUp(self):
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
    
    def test_extractor_initialization(self):
        """Test that extractor initializes correctly"""
        self.assertIsInstance(self.extractor, DataExtractor)
    
    def test_transformer_initialization(self):
        """Test that transformer initializes correctly"""
        self.assertIsInstance(self.transformer, DataTransformer)
    
    def test_parse_air_date(self):
        """Test air date parsing"""
        result = self.transformer.parse_air_date("January 11, 1983")
        self.assertEqual(result['year'], 1983)
        self.assertEqual(result['month'], 1)
        self.assertEqual(result['day'], 11)
        self.assertEqual(result['month_name'], 'january')
        
        result = self.transformer.parse_air_date("Invalid Date")
        self.assertEqual(result['year'], 1983)
        self.assertEqual(result['month'], 1)
        self.assertEqual(result['day'], 1)
    
    def test_clean_title(self):
        """Test title cleaning"""
        result = self.transformer.clean_title('"A Walk in the Woods"')
        self.assertEqual(result, 'A Walk In The Woods')
        
        result = self.transformer.clean_title('')
        self.assertEqual(result, '')
    
    def test_normalize_color_name(self):
        """Test color name normalization"""
        result = self.transformer.normalize_color_name('prussian blue\r\n')
        self.assertEqual(result, 'Prussian Blue')
        
        result = self.transformer.normalize_color_name('')
        self.assertEqual(result, '')
    
    def test_normalize_subject_name(self):
        """Test subject name normalization"""
        result = self.transformer.normalize_subject_name('mt. mckinley')
        self.assertEqual(result, 'Mount mckinley')
        
        result = self.transformer.normalize_subject_name('')
        self.assertEqual(result, '')

if __name__ == '__main__':
    unittest.main()
