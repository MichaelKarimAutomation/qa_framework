test:
	pytest tests/ -v

smoke:
	pytest tests/ -v -m smoke

report:
	allure serve reports/allure-results

clean:
	rmdir /s /q reports
