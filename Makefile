all: init test
.PHONY: all

init:
	pip install -r requirements.txt

test:
	python -m unittest tests/test_togglu.py

