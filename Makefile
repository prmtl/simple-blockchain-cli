.PHONY: requirements.txt format-code

requirements.txt:
	pip-compile --generate-hashes --output-file=requirements.txt requirements.in

format-code:
	black .

tests:
	py.test -vvv --black --isort --flake8
