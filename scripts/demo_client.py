#!/usr/bin/env python3
"""
Demo client script to test the sentiment analysis API.
This script sends sample tweets to the API and displays the results.
"""

import requests
import json
import sys
import argparse
import time

def analyze_tweets(tweets, api_url='http://localhost:5000/api/sentiment/analyze'):
    """Send tweets to the API for sentiment analysis.
    
    Args:
        tweets (list): A list of tweet strings to analyze.
        api_url (str): The URL of the sentiment analysis API endpoint.
        
    Returns:
        dict: A dictionary mapping tweets to their sentiment scores.
    """
    headers = {'Content-Type': 'application/json'}
    payload = {'tweets': tweets}
    
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}")
        return None

def display_results(results):
    """Display the sentiment analysis results in a readable format.
    
    Args:
        results (dict): A dictionary mapping tweets to their sentiment scores.
    """
    if not results:
        print("No results to display.")
        return
    
    print("\n" + "="*80)
    print(" SENTIMENT ANALYSIS RESULTS ".center(80, "="))
    print("="*80 + "\n")
    
    for tweet, score in results.items():
        # Determine sentiment category based on score
        if score > 0.5:
            sentiment = "Very Positive"
            symbol = "😄"
        elif score > 0:
            sentiment = "Positive"
            symbol = "🙂"
        elif score < -0.5:
            sentiment = "Very Negative"
            symbol = "😠"
        elif score < 0:
            sentiment = "Negative"
            symbol = "😐"
        else:
            sentiment = "Neutral"
            symbol = "😐"
        
        # Print the result
        print(f"Tweet: {tweet}")
        print(f"Score: {score:.4f} - {sentiment} {symbol}")
        print("-"*80)
    
    print("\n")

def main():
    """Main function to run the demo client."""
    parser = argparse.ArgumentParser(description='Demo client for the sentiment analysis API.')
    parser.add_argument('--api-url', default='http://localhost:5000/api/sentiment/analyze',
                        help='URL of the sentiment analysis API endpoint')
    parser.add_argument('--tweets', nargs='+', help='Tweets to analyze (space-separated)')
    args = parser.parse_args()
    
    # Use provided tweets or sample tweets
    if args.tweets:
        tweets = args.tweets
    else:
        # Sample tweets with different sentiments
        tweets = [
            "I love this new product! It's amazing!",
            "This is terrible, I'm very disappointed.",
            "The service was okay, nothing special.",
            "Great customer service and fast delivery.",
            "The product arrived damaged and customer service was unhelpful.",
            "I'm really enjoying using this app, it's so intuitive!",
            "This update has made everything worse, I can't find anything now.",
            "Just a normal day, nothing exciting happened."
        ]
    
    print(f"Analyzing {len(tweets)} tweets...")
    
    # Analyze the tweets
    start_time = time.time()
    results = analyze_tweets(tweets, args.api_url)
    end_time = time.time()
    
    # Display the results
    if results:
        display_results(results)
        print(f"Analysis completed in {end_time - start_time:.2f} seconds.")
    else:
        print("Failed to analyze tweets.")
        sys.exit(1)

if __name__ == "__main__":
    main() 