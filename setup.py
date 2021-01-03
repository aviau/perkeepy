from setuptools import find_packages
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description: str = f.read()

setup(
    name="perkeepy",
    version="0.1.7",
    author="Alexandre Viau",
    author_email="alexandre@alexandreviau.net",
    description="Python utilities for Perkeep",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aviau/perkeepy",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(),
    install_requires=[],
)
