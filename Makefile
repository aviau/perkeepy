.PHONY: all
all: test lint

venv: requirements.txt requirements.test.txt
	python -m venv venv
	venv/bin/pip install -r requirements.txt -r requirements.test.txt
	venv/bin/python setup.py develop

.PHONY: test
test: venv
	venv/bin/pytest perkeepy

.PHONY: lint
lint: venv
	venv/bin/mypy \
	    --config-file=mypy.ini \
		--cache-dir=.mypy_cache \
	    perkeepy

.PHONY: upload
upload: venv
	venv/bin/pip install twine==3.3.0 build==0.1.0
	rm -rf dist
	venv/bin/python -m build --sdist --wheel --outdir dist/
	venv/bin/python -m twine upload dist/*

.PHONY: clean
clean:
	rm -rf venv
	rm -rf build
	rm -rf dist
	rm -rf .mypy_cache
