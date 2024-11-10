from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hack4u-subiendo",
    version= "0.8.0",
    packages=find_packages(),
    install_requires=[],
    author="Test User",
    description="A library to list courses on hack4u",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io"
)
