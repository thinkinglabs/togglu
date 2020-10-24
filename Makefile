all: init test
.PHONY: init all

init:
	pip install -r requirements.txt

test:
	flake8 ./togglu ./tests
	python -m unittest -v
