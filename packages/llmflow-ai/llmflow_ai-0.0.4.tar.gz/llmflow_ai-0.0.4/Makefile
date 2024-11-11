.PHONY: hooks
hooks:
	pre-commit install

.PHONY: clean
clean:
	rm -Rf dist/*

.PHONY: dist
dist:
	python3 -m build

.PHONY: upload
upload:
	python3 -m twine upload --repository llmflow-ai dist/*

.PHONY: check
check:
	ruff check --fix
	ruff format
	mypy --exclude tests/test_package src tests

.PHONY: test
test:
	pytest
