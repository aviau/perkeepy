venv: requirements.txt
	python3.8 -m venv venv
	venv/bin/pip install -r requirements.txt
	venv/bin/python setup.py install

.PHONY: clean
clean:
	rm -rf venv
	rm -rf build
	rm -rf dist

.PHONY: upload
upload: venv
	venv/bin/pip install twine==3.3.0 wheel==0.36.2
	rm -rf dist
	venv/bin/python setup.py sdist bdist_wheel
	venv/bin/python -m twine upload dist/*
