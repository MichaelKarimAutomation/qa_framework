test:
	rmdir /s /q reports & pytest tests/ -v

smoke:
	pytest tests/ -v -m smoke

report:
	allure serve reports/allure-results

clean:
	rmdir /s /q reports

parallel:
	pytest tests/ -v -n auto
