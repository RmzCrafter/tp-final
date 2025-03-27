import os
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
import matplotlib.pyplot as plt
import seaborn as sns
from app.config.config import MODEL_PATH, TEST_SIZE, RANDOM_STATE
from app.utils.db_utils import get_training_data

class SentimentModel:
    def __init__(self):
        """Initialize the sentiment analysis model."""
        self.model_positive = None
        self.model_negative = None
        self.load_or_train_model()

    def load_or_train_model(self):
        """Load the model from disk if it exists, otherwise train a new model."""
        model_dir = os.path.dirname(MODEL_PATH)
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        
        if os.path.exists(f"{MODEL_PATH}_positive.pkl") and os.path.exists(f"{MODEL_PATH}_negative.pkl"):
            try:
                with open(f"{MODEL_PATH}_positive.pkl", 'rb') as f:
                    self.model_positive = pickle.load(f)
                with open(f"{MODEL_PATH}_negative.pkl", 'rb') as f:
                    self.model_negative = pickle.load(f)
                return
            except Exception as e:
                print(f"Error loading model: {e}")
                # Fall back to training a new model
        
        self.train_model()

    def preprocess_text(self, texts):
        """Preprocess the text data for model training and prediction."""
        # This is a simple implementation. In a production system, you would want to
        # implement more sophisticated text preprocessing here.
        return [text.lower() for text in texts]

    def train_model(self):
        """Train the sentiment analysis model."""
        # Get training data from the database
        df = get_training_data()
        
        if df.empty or len(df) < 10:
            print("Not enough training data. Using default model.")
            # Create simple models with default parameters
            self.model_positive = Pipeline([
                ('tfidf', TfidfVectorizer(max_features=5000)),
                ('clf', LogisticRegression(random_state=RANDOM_STATE))
            ])
            self.model_negative = Pipeline([
                ('tfidf', TfidfVectorizer(max_features=5000)),
                ('clf', LogisticRegression(random_state=RANDOM_STATE))
            ])
            # Fit with dummy data
            dummy_X = ["This is a positive text", "This is a negative text"]
            dummy_y_pos = [1, 0]
            dummy_y_neg = [0, 1]
            self.model_positive.fit(dummy_X, dummy_y_pos)
            self.model_negative.fit(dummy_X, dummy_y_neg)
        else:
            # Preprocess text
            X = self.preprocess_text(df['text'].tolist())
            y_positive = df['positive'].values
            y_negative = df['negative'].values
            
            # Split data into training and testing sets
            X_train, X_test, y_pos_train, y_pos_test, y_neg_train, y_neg_test = train_test_split(
                X, y_positive, y_negative, test_size=TEST_SIZE, random_state=RANDOM_STATE
            )
            
            # Create and train the positive sentiment model
            self.model_positive = Pipeline([
                ('tfidf', TfidfVectorizer(max_features=5000)),
                ('clf', LogisticRegression(random_state=RANDOM_STATE))
            ])
            self.model_positive.fit(X_train, y_pos_train)
            
            # Create and train the negative sentiment model
            self.model_negative = Pipeline([
                ('tfidf', TfidfVectorizer(max_features=5000)),
                ('clf', LogisticRegression(random_state=RANDOM_STATE))
            ])
            self.model_negative.fit(X_train, y_neg_train)
            
            # Evaluate the models
            self.evaluate_model(X_test, y_pos_test, y_neg_test)
        
        # Save the models
        with open(f"{MODEL_PATH}_positive.pkl", 'wb') as f:
            pickle.dump(self.model_positive, f)
        with open(f"{MODEL_PATH}_negative.pkl", 'wb') as f:
            pickle.dump(self.model_negative, f)

    def evaluate_model(self, X_test, y_pos_test, y_neg_test):
        """Evaluate the model performance and generate confusion matrices."""
        # Predict on test data
        y_pos_pred = self.model_positive.predict(X_test)
        y_neg_pred = self.model_negative.predict(X_test)
        
        # Generate confusion matrices
        cm_positive = confusion_matrix(y_pos_test, y_pos_pred)
        cm_negative = confusion_matrix(y_neg_test, y_neg_pred)
        
        # Calculate precision, recall, and F1-score
        precision_pos, recall_pos, f1_pos, _ = precision_recall_fscore_support(y_pos_test, y_pos_pred, average='binary')
        precision_neg, recall_neg, f1_neg, _ = precision_recall_fscore_support(y_neg_test, y_neg_pred, average='binary')
        
        # Save evaluation metrics
        metrics = {
            'positive': {
                'precision': precision_pos,
                'recall': recall_pos,
                'f1_score': f1_pos
            },
            'negative': {
                'precision': precision_neg,
                'recall': recall_neg,
                'f1_score': f1_neg
            }
        }
        
        with open(os.path.join(os.path.dirname(MODEL_PATH), 'evaluation_metrics.pkl'), 'wb') as f:
            pickle.dump(metrics, f)
        
        # Plot and save confusion matrices
        self._plot_confusion_matrix(cm_positive, 'Positive Sentiment Confusion Matrix', 
                                   os.path.join(os.path.dirname(MODEL_PATH), 'confusion_matrix_positive.png'))
        self._plot_confusion_matrix(cm_negative, 'Negative Sentiment Confusion Matrix', 
                                   os.path.join(os.path.dirname(MODEL_PATH), 'confusion_matrix_negative.png'))
        
        print(f"Model evaluation completed. Metrics saved to {os.path.dirname(MODEL_PATH)}")

    def _plot_confusion_matrix(self, cm, title, save_path):
        """Plot and save a confusion matrix."""
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Negative', 'Positive'], 
                   yticklabels=['Negative', 'Positive'])
        plt.title(title)
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()

    def predict_sentiment(self, texts):
        """Predict sentiment scores for a list of texts."""
        # Ensure models are loaded
        if self.model_positive is None or self.model_negative is None:
            self.load_or_train_model()
        
        # Preprocess texts
        processed_texts = self.preprocess_text(texts)
        
        # Predict positive and negative probabilities
        pos_probs = self.model_positive.predict_proba(processed_texts)[:, 1]
        neg_probs = self.model_negative.predict_proba(processed_texts)[:, 1]
        
        # Calculate sentiment scores between -1 and 1
        # Positive sentiment increases the score, negative sentiment decreases it
        sentiment_scores = pos_probs - neg_probs
        
        return sentiment_scores

    def retrain_model(self):
        """Retrain the model with the latest data."""
        print("Retraining sentiment analysis model...")
        self.train_model()
        print("Model retraining completed.")

# Singleton instance of the model
model_instance = None

def get_model_instance():
    """Get the singleton instance of the SentimentModel."""
    global model_instance
    if model_instance is None:
        model_instance = SentimentModel()
    return model_instance
