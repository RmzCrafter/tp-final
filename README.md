# SocialMetrics AI - Tweet Sentiment Analysis API

A RESTful API for analyzing sentiment in tweets, developed for SocialMetrics AI. This service enables real-time sentiment analysis of tweets, providing scores that range from -1 (very negative) to 1 (very positive).

## Features

- 🚀 Flask-based API for sentiment analysis
- 🧠 Machine learning model using logistic regression (scikit-learn)
- 🗄️ MySQL database for storing annotated tweets
- 🔄 Automated weekly model retraining
- 📊 Performance evaluation with confusion matrices and metrics
- 📈 PDF report generation of model performance
- 🐳 Docker support for easy deployment
- 🛠️ Makefile for simplified commands

## Requirements

- Python 3.7+
- MySQL Server
- Docker (optional)
- Make (optional)
- Python packages as listed in `requirements.txt`

## Installation

### Using Make (Recommended)

If you have Make installed, you can use the following commands:

```bash
# Install dependencies and setup database
make setup

# Run the application
make run
```

For Docker:

```bash
# Build and start Docker containers, then setup the database
make docker-build
make docker-setup
```

### Standard Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root directory with the following variables:

   ```
   DB_HOST=localhost
   DB_USER=your_mysql_user
   DB_PASSWORD=your_mysql_password
   DB_NAME=sentiment_analysis
   DB_PORT=3306
   DEBUG=True
   PORT=5000
   HOST=0.0.0.0
   MODEL_PATH=data/sentiment_model.pkl
   RETRAIN_INTERVAL_DAYS=7
   TEST_SIZE=0.2
   RANDOM_STATE=42
   ```

5. Set up the database and load sample data:
   ```bash
   python db/setup_db.py
   ```

### Docker Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Build and start the containers:

   ```bash
   docker-compose up -d
   ```

3. Initialize the database and load sample data:

   ```bash
   docker-compose exec app python db/setup_db.py
   ```

## Running the Application

### Using Make

```bash
make run
```

For Docker:

```bash
make docker-up
```

### Standard Method

Start the Flask application:

```bash
python app/app.py
```

### Using Docker

If you're using Docker, the application starts automatically when you run `docker-compose up`. To restart:

```bash
docker-compose restart app
```

The API will be available at `http://localhost:5000`.

## API Usage

### Analyze Sentiment

**Endpoint:** `POST /api/sentiment/analyze`

**Request:**

```json
{
  "tweets": [
    "I love this new product! It's amazing!",
    "This is terrible, I'm very disappointed.",
    "The service was okay, nothing special."
  ]
}
```

**Response:**

```json
{
  "I love this new product! It's amazing!": 0.85,
  "This is terrible, I'm very disappointed.": -0.72,
  "The service was okay, nothing special.": 0.05
}
```

**Curl Example:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"tweets": ["I love this product!", "This is terrible!"]}' http://localhost:5000/api/sentiment/analyze
```

### Demo Client

You can use the provided demo client to test the API:

```bash
python scripts/demo_client.py
# Or using Make
make demo
```

Or with custom tweets:

```bash
python scripts/demo_client.py --tweets "I love this product!" "This is terrible!" "The service was okay"
```

With Docker:

```bash
docker-compose exec app python scripts/demo_client.py
```

## Available Make Commands

| Command             | Description                             |
| ------------------- | --------------------------------------- |
| `make setup`        | Install requirements and setup database |
| `make run`          | Run the Flask application               |
| `make test`         | Run the test suite                      |
| `make clean`        | Clean up generated files                |
| `make docker-build` | Build Docker containers                 |
| `make docker-up`    | Start Docker containers                 |
| `make docker-down`  | Stop Docker containers                  |
| `make docker-setup` | Setup database in Docker                |
| `make train`        | Train the sentiment model               |
| `make report`       | Generate evaluation report              |
| `make demo`         | Run the demo client                     |
| `make help`         | Show help for make commands             |

## Database Schema

The sentiment analysis service uses a MySQL database with the following schema:

### Table: tweets

| Column     | Type      | Description                              |
| ---------- | --------- | ---------------------------------------- |
| id         | INT       | Primary key, auto-increment              |
| text       | TEXT      | Content of the tweet                     |
| positive   | TINYINT   | 1 if the tweet is positive, 0 otherwise  |
| negative   | TINYINT   | 1 if the tweet is negative, 0 otherwise  |
| created_at | TIMESTAMP | When the tweet was added to the database |

Tweets can be:

- Positive (positive=1, negative=0)
- Negative (positive=0, negative=1)
- Mixed (positive=1, negative=1)
- Neutral (positive=0, negative=0)

## Model Architecture

The sentiment analysis model uses two separate logistic regression classifiers:

1. **Positive Sentiment Model**: Predicts whether a tweet expresses positive sentiment
2. **Negative Sentiment Model**: Predicts whether a tweet expresses negative sentiment

The models use TF-IDF vectorization to convert text into numerical features. The final sentiment score is calculated as:

```
sentiment_score = positive_probability - negative_probability
```

This results in a score between -1 (very negative) and 1 (very positive).

## Model Retraining

The model is automatically retrained every week by the scheduler. To manually retrain the model, run:

```bash
python scripts/retrain_model.py
# Or using Make
make train
```

With Docker:

```bash
docker-compose exec app python scripts/retrain_model.py
```

To set up a cron job for weekly retraining (Linux/Unix):

```bash
crontab -e
```

Add the following line to run the script every Sunday at 2:00 AM:

```
0 2 * * 0 /path/to/python /path/to/scripts/retrain_model.py
```

## Evaluation and Reporting

The model evaluation metrics and confusion matrices are saved in the `data` directory when the model is retrained. You can generate a comprehensive PDF report with:

```bash
python scripts/generate_report.py
# Or using Make
make report
```

With Docker:

```bash
docker-compose exec app python scripts/generate_report.py
```

The report includes:

- Confusion matrices for positive and negative sentiment
- Precision, recall, and F1-score metrics
- Strengths and weaknesses analysis
- Recommendations for improvement

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── config/
│   │   └── config.py
│   ├── controllers/
│   │   └── sentiment_controller.py
│   ├── models/
│   │   └── sentiment_model.py
│   └── utils/
│       ├── db_utils.py
│       └── scheduler.py
├── data/
├── db/
│   └── setup_db.py
├── reports/
│   └── evaluation_report.md
├── scripts/
│   └── retrain_model.py
├── .env
├── README.md
└── requirements.txt
```

## Testing

Run the tests to verify the API functionality:

```bash
python scripts/run_tests.py
# Or using Make
make test
```

With Docker:

```bash
docker-compose exec app python scripts/run_tests.py
```

## Performance Considerations

The sentiment analysis model balances accuracy with speed to provide real-time sentiment analysis for tweets. For production environments, consider:

1. **Database Scaling**: For large volumes of tweets, consider database sharding or replication
2. **API Load Balancing**: Use multiple API instances behind a load balancer
3. **Batch Processing**: For analyzing large numbers of tweets, use batch processing
4. **Caching**: Implement caching for frequently analyzed tweets

## Troubleshooting

### Common Issues

1. **MySQL Connection Error**

   - Check that MySQL is running and accessible
   - Verify that the database credentials in `.env` are correct
   - For Docker: ensure the MySQL container is running with `docker-compose ps`

2. **Model Training Error**

   - Ensure you have sufficient annotated tweets in the database
   - Check disk space for saving model files

3. **API Not Responding**
   - Verify that the Flask application is running
   - Check the port configuration in `.env`
   - For Docker: check container logs with `docker-compose logs app`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- scikit-learn for machine learning functionality
- Flask for the web framework
- PyMySQL for database connectivity
