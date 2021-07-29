.PHONY: all
all: test lint

venv: requirements.txt requirements.test.txt
	rm -rf venv
	python -m venv venv
	venv/bin/pip install -r requirements.txt -r requirements.test.txt
	venv/bin/python setup.py develop

.PHONY: test
test: venv
	venv/bin/pytest perkeepy -v

.PHONY: fmt
fmt: format

.PHONY: format
format: venv
	venv/bin/black \
	    --config=pyproject.toml \
	    perkeepy setup.py
	venv/bin/isort \
	    --settings-path=pyproject.toml \
	    perkeepy

.PHONY: mypy
mypy: venv
	venv/bin/mypy \
	    --config-file=mypy.ini \
	    --cache-dir=.mypy_cache \
	    perkeepy setup.py

.PHONY: check-copyright
check-copyright: venv
	find perkeepy \
	    | grep "\.py$$" \
	    | xargs \
	        -d '\n' \
	        venv/bin/python perkeepy/scripts/copyrightify.py \
	            --check

.PHONY: lint
lint: venv mypy check-copyright
	venv/bin/black \
	    --config=pyproject.toml \
	    --check \
	    perkeepy setup.py
	venv/bin/isort \
	    --settings-path=pyproject.toml \
	    --check \
	    --diff \
	    perkeepy

.PHONY: build
build: venv
	venv/bin/pip install twine==3.4.2 build==0.5.1
	rm -rf dist
	venv/bin/python -m build --sdist --wheel --outdir dist/

.PHONY: clean
clean:
	rm -rf venv
	rm -rf build
	rm -rf dist
	rm -rf .mypy_cache
