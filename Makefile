.PHONY: install preprocess analyze test clean

install:
	pip install -e ".[dev]"

preprocess:
	python scripts/preprocess.py

analyze:
	python scripts/analyze.py

test:
	pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf *.egg-info src/*.egg-info
