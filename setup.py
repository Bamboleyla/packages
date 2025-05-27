"""setup for installing necessary packages and dependencies."""

from setuptools import setup, find_packages

setup(
    name="myLib",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "asyncio==3.4.3",
        "certifi==2025.1.31",
        "charset-normalizer==3.4.1",
        "idna==3.10",
        "numpy==2.2.3",
        "pandas==2.2.3",
        "python-dateutil==2.9.0.post0",
        "python-dotenv==1.0.1",
        "pytz==2025.1",
        "requests==2.32.3",
        "setuptools==76.0.0",
        "six==1.17.0",
        "tzdata==2025.1",
        "urllib3==2.3.0",
        "websockets==15.0.1",
    ],
    python_requires=">=3.13.2",
)

# To update the list of dependencies, it is unurumitated to execute: pip freeze > requirements.txt
# To create library: python setup.py sdist bdist_wheel
