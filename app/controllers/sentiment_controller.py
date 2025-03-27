from flask import Blueprint, request, jsonify
from app.models.sentiment_model import get_model_instance

# Create a Blueprint for the sentiment analysis routes
sentiment_bp = Blueprint('sentiment', __name__)

@sentiment_bp.route('/analyze', methods=['POST'])
def analyze_sentiment():
    """Analyze the sentiment of a list of tweets.
    
    Expects a JSON payload with a 'tweets' key containing a list of strings.
    Returns a JSON object with each tweet as a key and its sentiment score as a value.
    """
    # Get the request data
    data = request.get_json()
    
    # Validate the request data
    if not data or 'tweets' not in data:
        return jsonify({'error': 'Missing required field: tweets'}), 400
    
    tweets = data['tweets']
    
    # Validate the tweets data
    if not isinstance(tweets, list):
        return jsonify({'error': 'Tweets must be a list of strings'}), 400
    
    if not all(isinstance(tweet, str) for tweet in tweets):
        return jsonify({'error': 'All tweets must be strings'}), 400
    
    if len(tweets) == 0:
        return jsonify({'error': 'Tweets list cannot be empty'}), 400
    
    # Get the model instance
    model = get_model_instance()
    
    # Predict sentiment scores
    sentiment_scores = model.predict_sentiment(tweets)
    
    # Create a dictionary of tweets and their scores
    results = {tweet: float(score) for tweet, score in zip(tweets, sentiment_scores)}
    
    return jsonify(results), 200
