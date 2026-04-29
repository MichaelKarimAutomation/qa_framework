report:
	allure serve reports/allure-results

clean:
	python scripts/clean.py

test:
	python scripts/clean.py & pytest tests/ -v --env=uat

smoke:
	pytest tests/ -v -m smoke --env=uat

parallel:
	pytest tests/ -v -n auto --env=uat

lint:
	ruff check .

format:
	ruff format .

docker-build:
	docker build -t qa-framework .

docker-run:
	docker run --rm qa-framework
	