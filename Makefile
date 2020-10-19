all: init test
.PHONY: init all

init:
	pip install -r requirements.txt

test:
	python -m unittest -v


