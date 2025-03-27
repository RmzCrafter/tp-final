import pymysql
from app.config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT
import pandas as pd

def get_db_connection():
    """Create a connection to the MySQL database."""
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print(f"Error connecting to MySQL database: {e}")
        raise

def create_tables():
    """Create the necessary tables if they don't exist."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Create tweets table for storing annotated tweets
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tweets (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    text TEXT NOT NULL,
                    positive TINYINT NOT NULL DEFAULT 0,
                    negative TINYINT NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)
        connection.commit()
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise
    finally:
        connection.close()

def get_training_data():
    """Get all annotated tweets from the database for model training."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT text, positive, negative FROM tweets")
            tweets = cursor.fetchall()
        return pd.DataFrame(tweets)
    except Exception as e:
        print(f"Error getting training data: {e}")
        raise
    finally:
        connection.close()

def save_tweet(text, positive=0, negative=0):
    """Save a new annotated tweet to the database."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)"
            cursor.execute(sql, (text, positive, negative))
        connection.commit()
    except Exception as e:
        print(f"Error saving tweet: {e}")
        raise
    finally:
        connection.close()

def get_recent_tweets(limit=1000):
    """Get the most recent annotated tweets from the database."""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT text, positive, negative 
                FROM tweets 
                ORDER BY created_at DESC 
                LIMIT %s
            """, (limit,))
            tweets = cursor.fetchall()
        return pd.DataFrame(tweets)
    except Exception as e:
        print(f"Error getting recent tweets: {e}")
        raise
    finally:
        connection.close()
