from setuptools import find_packages
from setuptools import setup

setup(
    name="perkeepy",
    version="0.1",
    author="Alexandre Viau",
    author_email="alexandre@alexandreviau.net",
    description="Python utilities for Perkeep",
    url="https://github.com/aviau/perkeepy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(),
    install_requires=[],
)
