.PHONY: help report clean docs test smoke regression parallel lint format docker-build docker-run

help: # List all available commands
	python scripts/help.py

report: # Serve Allure test report in browser
	allure serve reports/allure-results

clean: # Delete generated reports
	python scripts/delete_reports.py

docs: # Generate HTML API documentation under docs/_build/html
	python scripts/generate_docs.py

test: # Run full test suite after deleting reports folder
	python scripts/delete_reports.py & pytest tests/ -v

smoke: # Run smoke-tagged tests only
	pytest tests/ -v -m smoke

regression: # Run regression-tagged tests only
	pytest tests/ -v -m regression

parallel: # Run full test suite in parallel
	pytest tests/ -v -n auto

lint: # Check code style with ruff
	ruff check .

format: # Auto-format code with ruff
	ruff format .

docker-build: # Build the Docker image
	docker build -t qa-framework .

docker-run: # Run the Docker container with .env vars
	docker run --rm --env-file .env qa-framework
