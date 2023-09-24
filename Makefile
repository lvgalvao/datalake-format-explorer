install:
	poetry install
format:
	isort .
	black .
test:
	pytest -v
kill:
	kill -9 $(shell lsof -t -i :8000)
