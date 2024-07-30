black:
	isort pkgs/core.py
	black -l 79 pkgs/core.py
	isort pkgs/main.py
	black -l 79 pkgs/main.py

clean:
	find . -type d -name __pycache__ | xargs rm -rf

ready:
	[ -d pdfs ] || mkdir pdfs; \
	[ -d brew ] || mkdir brew; \
	python3 -m venv venv; \
	. venv/bin/activate; \
	pip install -U pip; \
	pip install -r requirements.txt; \
	deactivate

.PHONY: black clean ready
