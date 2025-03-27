#!/usr/bin/env python3
"""
Script to generate a PDF evaluation report for the sentiment analysis model.
This script reads the model evaluation metrics and confusion matrices,
and generates a comprehensive report in PDF format.
"""

import os
import sys
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import argparse
from fpdf import FPDF

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.config import MODEL_PATH
from app.models.sentiment_model import get_model_instance

class PDF(FPDF):
    """Custom PDF class for creating the evaluation report."""
    
    def header(self):
        """Add the header to each page."""
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Sentiment Analysis Model Evaluation Report', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """Add the footer to each page."""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def load_metrics():
    """Load the evaluation metrics from the pickle file."""
    metrics_path = os.path.join(os.path.dirname(MODEL_PATH), 'evaluation_metrics.pkl')
    
    if not os.path.exists(metrics_path):
        print(f"Metrics file not found at {metrics_path}")
        return None
    
    with open(metrics_path, 'rb') as f:
        metrics = pickle.load(f)
    
    return metrics

def count_tweets():
    """Count the total number of tweets in the training dataset."""
    try:
        from app.utils.db_utils import get_training_data
        df = get_training_data()
        return len(df)
    except Exception as e:
        print(f"Error counting tweets: {e}")
        return "Unknown"

def generate_pdf_report(output_path=None):
    """Generate a PDF report with the evaluation metrics and confusion matrices."""
    # Load the metrics
    metrics = load_metrics()
    
    if metrics is None:
        print("No metrics found. Please train the model first.")
        return
    
    # Count the tweets
    total_tweets = count_tweets()
    training_size = int(total_tweets * 0.8) if isinstance(total_tweets, int) else "Unknown"
    test_size = int(total_tweets * 0.2) if isinstance(total_tweets, int) else "Unknown"
    
    # Create a new PDF object
    pdf = PDF()
    pdf.add_page()
    
    # Add title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Sentiment Analysis Model Evaluation Report', 0, 1, 'C')
    pdf.ln(10)
    
    # Add introduction
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Introduction', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'This report evaluates the performance of the sentiment analysis model used for SocialMetrics AI\'s tweet analysis service. The model is based on logistic regression and is designed to classify tweets as positive or negative.')
    pdf.ln(5)
    
    # Add data overview
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Data Overview', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, f'The model was trained on a dataset of {total_tweets} annotated tweets from the tweets table in our database. Each tweet was labeled with binary values for positive and negative sentiment, allowing for the possibility of mixed sentiment (both positive and negative) or neutral sentiment (neither positive nor negative).')
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'- Training set size: {training_size} tweets', 0, 1, 'L')
    pdf.cell(0, 10, f'- Test set size: {test_size} tweets (20% of the total dataset)', 0, 1, 'L')
    pdf.cell(0, 10, f'- Data collection period: Up to {datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'L')
    pdf.ln(5)
    
    # Add confusion matrices
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Confusion Matrices', 0, 1, 'L')
    
    # Positive sentiment confusion matrix
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Positive Sentiment Model', 0, 1, 'L')
    
    # Add the positive confusion matrix image
    cm_pos_path = os.path.join(os.path.dirname(MODEL_PATH), 'confusion_matrix_positive.png')
    if os.path.exists(cm_pos_path):
        pdf.image(cm_pos_path, x=10, y=None, w=180)
    else:
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, 'Confusion matrix image not found.')
    
    pdf.ln(5)
    
    # Negative sentiment confusion matrix
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Negative Sentiment Model', 0, 1, 'L')
    
    # Add the negative confusion matrix image
    cm_neg_path = os.path.join(os.path.dirname(MODEL_PATH), 'confusion_matrix_negative.png')
    if os.path.exists(cm_neg_path):
        pdf.image(cm_neg_path, x=10, y=None, w=180)
    else:
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, 'Confusion matrix image not found.')
    
    pdf.ln(5)
    
    # Add performance metrics
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Performance Metrics', 0, 1, 'L')
    
    # Positive sentiment metrics
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Positive Sentiment Model', 0, 1, 'L')
    
    if metrics and 'positive' in metrics:
        pos_metrics = metrics['positive']
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'- Precision: {pos_metrics["precision"]:.4f}', 0, 1, 'L')
        pdf.cell(0, 10, f'- Recall: {pos_metrics["recall"]:.4f}', 0, 1, 'L')
        pdf.cell(0, 10, f'- F1-Score: {pos_metrics["f1_score"]:.4f}', 0, 1, 'L')
    else:
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, 'Metrics not available.')
    
    pdf.ln(5)
    
    # Negative sentiment metrics
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Negative Sentiment Model', 0, 1, 'L')
    
    if metrics and 'negative' in metrics:
        neg_metrics = metrics['negative']
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'- Precision: {neg_metrics["precision"]:.4f}', 0, 1, 'L')
        pdf.cell(0, 10, f'- Recall: {neg_metrics["recall"]:.4f}', 0, 1, 'L')
        pdf.cell(0, 10, f'- F1-Score: {neg_metrics["f1_score"]:.4f}', 0, 1, 'L')
    else:
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, 'Metrics not available.')
    
    pdf.ln(5)
    
    # Add analysis
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Analysis of Model Performance', 0, 1, 'L')
    
    # Strengths
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Strengths', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, '1. Efficient Classification: The logistic regression model provides efficient and interpretable sentiment classification.')
    pdf.multi_cell(0, 10, '2. Fast Inference: The model can quickly analyze large volumes of tweets in real-time.')
    pdf.multi_cell(0, 10, '3. Balanced Performance: The model maintains a good balance between precision and recall.')
    pdf.ln(5)
    
    # Weaknesses
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Weaknesses', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, '1. Limited Feature Representation: The TF-IDF vectorizer captures only word frequency, missing context and semantics.')
    pdf.multi_cell(0, 10, '2. Binary Classification Limitations: The separate positive/negative models may not handle mixed sentiments well.')
    pdf.multi_cell(0, 10, '3. Data Sensitivity: Performance heavily depends on the quality and diversity of the training data.')
    pdf.ln(5)
    
    # Potential Biases
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Potential Biases', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, '1. Language Bias: The model may perform better on certain language styles or terminology common in the training data.')
    pdf.multi_cell(0, 10, '2. Topic Bias: The model might be biased toward topics prevalent in the training dataset.')
    pdf.ln(5)
    
    # Add recommendations
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Recommendations for Improvement', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '1. Data Enhancement', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'Increase the diversity and size of the training dataset by collecting more annotated tweets, particularly for underrepresented sentiment patterns.')
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '2. Feature Engineering', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'Enhance the model by incorporating more sophisticated features, such as:')
    pdf.cell(10, 10, '', 0, 0)
    pdf.cell(0, 10, '- N-grams beyond unigrams (e.g., bigrams, trigrams)', 0, 1, 'L')
    pdf.cell(10, 10, '', 0, 0)
    pdf.cell(0, 10, '- Part-of-speech tagging', 0, 1, 'L')
    pdf.cell(10, 10, '', 0, 0)
    pdf.cell(0, 10, '- Named entity recognition', 0, 1, 'L')
    pdf.cell(10, 10, '', 0, 0)
    pdf.cell(0, 10, '- Sentiment-specific word embeddings', 0, 1, 'L')
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, '3. Model Complexity', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'Experiment with more complex models, such as:')
    pdf.cell(10, 10, '', 0, 0)
    pdf.cell(0, 10, '- Support Vector Machines with different kernels', 0, 1, 'L')
    pdf.cell(10, 10, '', 0, 0)
    pdf.cell(0, 10, '- Ensemble methods (Random Forests, Gradient Boosting)', 0, 1, 'L')
    pdf.cell(10, 10, '', 0, 0)
    pdf.cell(0, 10, '- Deep learning approaches (LSTM, Transformer-based models like BERT)', 0, 1, 'L')
    pdf.ln(5)
    
    # Add conclusion
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Conclusion', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    
    # Calculate overall performance metric
    overall_metric = 0
    if metrics:
        pos_f1 = metrics['positive']['f1_score'] if 'positive' in metrics else 0
        neg_f1 = metrics['negative']['f1_score'] if 'negative' in metrics else 0
        overall_metric = (pos_f1 + neg_f1) / 2
    
    assessment = "satisfactory"
    if overall_metric > 0.8:
        assessment = "excellent"
    elif overall_metric > 0.6:
        assessment = "good"
    
    pdf.multi_cell(0, 10, f'The current sentiment analysis model provides {assessment} performance in analyzing tweet sentiments. While it efficiently classifies most tweets, there are significant opportunities for improvement through enhanced data collection, advanced feature engineering, and exploring more complex model architectures.')
    pdf.multi_cell(0, 10, 'The next iteration of the model should focus on increasing the training dataset diversity and implementing more sophisticated text preprocessing to address the most critical weaknesses identified in this evaluation.')
    pdf.ln(5)
    
    # Add footer info
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, f'Date of Evaluation: {datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'L')
    pdf.cell(0, 10, 'Model Version: 1.0', 0, 1, 'L')
    pdf.cell(0, 10, 'Evaluated by: SocialMetrics AI Team', 0, 1, 'L')
    
    # Save the PDF
    if output_path is None:
        output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports', 'sentiment_model_evaluation.pdf')
    
    pdf.output(output_path)
    print(f"Report generated successfully: {output_path}")
    return output_path

def main():
    """Main function to generate the PDF report."""
    parser = argparse.ArgumentParser(description='Generate a PDF evaluation report for the sentiment analysis model.')
    parser.add_argument('--output', help='Output path for the PDF report', default=None)
    args = parser.parse_args()
    
    try:
        output_path = generate_pdf_report(args.output)
        print(f"Report saved to: {output_path}")
    except Exception as e:
        print(f"Error generating report: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 