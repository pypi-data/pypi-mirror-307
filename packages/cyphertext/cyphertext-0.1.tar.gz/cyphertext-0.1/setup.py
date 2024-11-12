# setup.py
from setuptools import setup, find_packages

setup(
    name="cyphertext",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "cryptography",  # This ensures the cryptography package is installed
    ],
    entry_points={
        'console_scripts': [
            'cyphertext-utils = cyphertext:main',  # Allows running the `main()` function via command line
        ],
    },
)