"""setup for installing necessary packages and dependencies."""

from setuptools import setup, find_packages

setup(
    name="packages",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=1.0.1",
        "setuptools>=76.0.0",
    ],
    python_requires=">=3.13.2",
)