install:
	poetry install
format:
	isort .
	black .
test:
	pytest -v
kill:
	kill -9 $(shell lsof -t -i :8000)
run:
	@if [ -z "$(artist)" ]; then \
		echo "Por favor, especifique o nome do artista: make run artist='Nome do Artista'"; \
		exit 1; \
	fi
	python -m app.pipeline "$(artist)"