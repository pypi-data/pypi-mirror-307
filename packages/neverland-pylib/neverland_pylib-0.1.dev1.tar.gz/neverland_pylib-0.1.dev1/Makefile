setup:
	virtualenv .venv -p python3.10
	./.venv/bin/pip install pip-tools

install:
	./.venv/bin/pip-compile --extra dev,compile -v
	./.venv/bin/pip-sync -v

release:
	rm -Rf ./dist
	python -m build
	twine upload dist/*

push:
	git add . && codegpt commit . && git push