test:
	rmdir /s /q reports & pytest tests/ -v --env=uat

smoke:
	pytest tests/ -v -m smoke --env=uat

parallel:
	pytest tests/ -v -n auto --env=uat

report:
	allure serve reports/allure-results

clean:
	rmdir /s /q reports
	