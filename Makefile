.all: test

venv: requirements.txt requirements.test.txt
	python3.8 -m venv venv
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
	venv/bin/pip install twine==3.3.0 wheel==0.36.2
	rm -rf dist
	venv/bin/python setup.py sdist bdist_wheel
	venv/bin/python -m twine upload dist/*

.PHONY: clean
clean:
	rm -rf venv
	rm -rf build
	rm -rf dist
	rm -rf .mypy_cache
