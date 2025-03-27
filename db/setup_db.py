import pymysql
import os
import sys
import pandas as pd

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

def setup_database():
    """Set up the MySQL database and tables."""
    print("Setting up the database...")
    
    # Connect to MySQL server without specifying a database
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        
        with connection.cursor() as cursor:
            # Create the database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"Database '{DB_NAME}' created or already exists.")
            
            # Switch to the newly created database
            cursor.execute(f"USE {DB_NAME}")
            
            # Create the tweets table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tweets (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    text TEXT NOT NULL,
                    positive TINYINT NOT NULL DEFAULT 0,
                    negative TINYINT NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)
            print("Table 'tweets' created or already exists.")
        
        connection.commit()
    except Exception as e:
        print(f"Error setting up database: {e}")
        sys.exit(1)
    finally:
        connection.close()
    
    print("Database setup completed.")

def load_sample_data():
    """Load sample data into the tweets table."""
    print("Loading sample data...")
    
    # Sample tweets with sentiment annotations
    sample_data = [
        {"text": "I love this new product! It's amazing!", "positive": 1, "negative": 0},
        {"text": "This is terrible, I'm very disappointed.", "positive": 0, "negative": 1},
        {"text": "The service was okay, nothing special.", "positive": 0, "negative": 0},
        {"text": "Great customer service and fast delivery.", "positive": 1, "negative": 0},
        {"text": "The product arrived damaged and customer service was unhelpful.", "positive": 0, "negative": 1},
        {"text": "I'm really enjoying using this app, it's so intuitive!", "positive": 1, "negative": 0},
        {"text": "This update has made everything worse, I can't find anything now.", "positive": 0, "negative": 1},
        {"text": "Just a normal day, nothing exciting happened.", "positive": 0, "negative": 0},
        {"text": "Absolutely thrilled with my purchase, best decision ever!", "positive": 1, "negative": 0},
        {"text": "Worst experience ever, will never use this service again.", "positive": 0, "negative": 1},
        {"text": "The new features are impressive, but there are still some bugs.", "positive": 1, "negative": 1},
        {"text": "I'm neutral about this product, it works as expected.", "positive": 0, "negative": 0},
        {"text": "Excellent value for money, highly recommend!", "positive": 1, "negative": 0},
        {"text": "Poor quality and overpriced, avoid at all costs.", "positive": 0, "negative": 1},
        {"text": "It's an average product, does the job but nothing special.", "positive": 0, "negative": 0}
    ]
    
    # Convert to DataFrame
    df = pd.DataFrame(sample_data)
    
    # Connect to the database
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        
        with connection.cursor() as cursor:
            # Check if there's already data in the table
            cursor.execute("SELECT COUNT(*) FROM tweets")
            count = cursor.fetchone()[0]
            
            if count > 0:
                print(f"Table 'tweets' already contains {count} records. Skipping sample data loading.")
                return
            
            # Insert sample data
            for _, row in df.iterrows():
                cursor.execute(
                    "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)",
                    (row['text'], row['positive'], row['negative'])
                )
            
            print(f"Inserted {len(df)} sample tweets into the database.")
        
        connection.commit()
    except Exception as e:
        print(f"Error loading sample data: {e}")
    finally:
        connection.close()
    
    print("Sample data loading completed.")

if __name__ == "__main__":
    setup_database()
    load_sample_data()
