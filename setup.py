from setuptools import setup, find_packages


test_packages = [
    "pytest>=5.4.3",
    "black>=19.10b0",
    "flake8>=3.8.3",
]

util_packages = ["jupyterlab>=2.2.0", "pre-commit>=2.6.0"]

docs_packages = [
    "mkdocs>=1.1",
    "mkdocs-material>=4.6.3",
    "mkdocstrings>=0.8.0",
]

dev_packages = test_packages + util_packages + docs_packages

setup(
    name="clumper",
    version="0.2.5",
    packages=find_packages(include=["clumper", "clumper.*"]),
    extras_require={"dev": dev_packages, "test": test_packages},
)
