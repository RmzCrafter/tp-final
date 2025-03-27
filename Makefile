.PHONY: setup run test clean docker-build docker-up docker-down docker-setup

# Standard installation and setup
setup:
	pip install -r requirements.txt
	python db/setup_db.py

# Run the Flask application
run:
	python app/app.py

# Run tests
test:
	python scripts/run_tests.py

# Clean up generated files
clean:
	rm -rf data/*.pkl data/*.png
	rm -rf reports/*.pdf
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-setup: docker-up
	docker-compose exec app python db/setup_db.py

# Model commands
train:
	python scripts/retrain_model.py

report:
	python scripts/generate_report.py

# Demo client
demo:
	python scripts/demo_client.py

# Help command
help:
	@echo "Available commands:"
	@echo "  make setup        - Install requirements and setup database"
	@echo "  make run          - Run the Flask application"
	@echo "  make test         - Run the test suite"
	@echo "  make clean        - Clean up generated files"
	@echo "  make docker-build - Build Docker containers"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make docker-setup - Setup database in Docker"
	@echo "  make train        - Train the sentiment model"
	@echo "  make report       - Generate evaluation report"
	@echo "  make demo         - Run the demo client" 