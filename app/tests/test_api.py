import os
import sys
import json
import unittest

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import create_app

class TestSentimentAPI(unittest.TestCase):
    """Test cases for the sentiment analysis API."""
    
    def setUp(self):
        """Set up the test client."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.client.testing = True
    
    def test_analyze_sentiment_valid(self):
        """Test the analyze sentiment endpoint with valid input."""
        # Test data
        tweets = ["I love this product!", "This is terrible!"]
        
        # Make a request to the API
        response = self.client.post(
            '/api/sentiment/analyze',
            data=json.dumps({'tweets': tweets}),
            content_type='application/json'
        )
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        
        # Parse the response data
        data = json.loads(response.data)
        
        # Check that all tweets are in the response
        for tweet in tweets:
            self.assertIn(tweet, data)
            
        # Check that the sentiment scores are within the expected range
        for tweet, score in data.items():
            self.assertGreaterEqual(score, -1)
            self.assertLessEqual(score, 1)
    
    def test_analyze_sentiment_empty(self):
        """Test the analyze sentiment endpoint with empty input."""
        # Make a request to the API with empty tweets list
        response = self.client.post(
            '/api/sentiment/analyze',
            data=json.dumps({'tweets': []}),
            content_type='application/json'
        )
        
        # Check the response
        self.assertEqual(response.status_code, 400)
        
        # Parse the response data
        data = json.loads(response.data)
        
        # Check the error message
        self.assertIn('error', data)
    
    def test_analyze_sentiment_missing_tweets(self):
        """Test the analyze sentiment endpoint with missing tweets."""
        # Make a request to the API without the 'tweets' key
        response = self.client.post(
            '/api/sentiment/analyze',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        # Check the response
        self.assertEqual(response.status_code, 400)
        
        # Parse the response data
        data = json.loads(response.data)
        
        # Check the error message
        self.assertIn('error', data)
    
    def test_analyze_sentiment_invalid_type(self):
        """Test the analyze sentiment endpoint with invalid input type."""
        # Make a request to the API with non-list tweets
        response = self.client.post(
            '/api/sentiment/analyze',
            data=json.dumps({'tweets': 'not a list'}),
            content_type='application/json'
        )
        
        # Check the response
        self.assertEqual(response.status_code, 400)
        
        # Parse the response data
        data = json.loads(response.data)
        
        # Check the error message
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main() 