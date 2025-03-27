#!/usr/bin/env python3
"""
Script to manually retrain the sentiment analysis model.
Can be used in a cron job for regular retraining.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.sentiment_model import get_model_instance
import argparse

def main():
    """Retrain the sentiment analysis model."""
    parser = argparse.ArgumentParser(description='Retrain the sentiment analysis model.')
    parser.add_argument('--force', action='store_true', help='Force retraining even if the model already exists.')
    args = parser.parse_args()
    
    print("Starting model retraining...")
    
    # Get the model instance
    model = get_model_instance()
    
    # Retrain the model
    model.retrain_model()
    
    print("Model retraining completed.")

if __name__ == "__main__":
    main()
