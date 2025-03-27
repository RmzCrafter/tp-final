from app import create_app
from app.config.config import HOST, PORT, DEBUG

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Run the application
    app.run(host=HOST, port=PORT, debug=DEBUG)
