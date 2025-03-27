#!/usr/bin/env python3
"""
Script simple pour générer un exemple de rapport PDF pour le dépôt GitHub.
"""

import os
from fpdf import FPDF

def generate_sample_report():
    """Generate a sample evaluation report PDF."""
    # Create directory if not exists
    os.makedirs('reports', exist_ok=True)
    
    # Create PDF object
    pdf = FPDF()
    pdf.add_page()
    
    # Add title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Sentiment Analysis Model Evaluation Report', 0, 1, 'C')
    pdf.ln(10)
    
    # Add introduction
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Introduction', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'This is a sample evaluation report for the sentiment analysis model used in the SocialMetrics AI project. This report demonstrates the format and content of the automatically generated reports.')
    pdf.ln(5)
    
    # Add data overview
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Data Overview', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'The model was trained on a dataset of 15 annotated tweets from the tweets table in our database. Each tweet was labeled with binary values for positive and negative sentiment.')
    pdf.ln(5)
    
    # Add sample metrics
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Performance Metrics', 0, 1, 'L')
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Positive Sentiment Model', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, '- Precision: 0.8500', 0, 1, 'L')
    pdf.cell(0, 10, '- Recall: 0.7800', 0, 1, 'L')
    pdf.cell(0, 10, '- F1-Score: 0.8136', 0, 1, 'L')
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Negative Sentiment Model', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, '- Precision: 0.7900', 0, 1, 'L')
    pdf.cell(0, 10, '- Recall: 0.8200', 0, 1, 'L')
    pdf.cell(0, 10, '- F1-Score: 0.8047', 0, 1, 'L')
    pdf.ln(5)
    
    # Add conclusion
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Conclusion', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'The current sentiment analysis model provides good performance in analyzing tweet sentiments. With continued data collection and model refinement, we expect further improvements in accuracy.')
    
    # Save the PDF
    output_path = 'reports/sentiment_model_evaluation_sample.pdf'
    pdf.output(output_path)
    print(f"Sample report generated at: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_sample_report() 