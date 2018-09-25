all: init test
.PHONY: all

init:
	pip install -r requirements.txt

test:
	./test_togglu.py

