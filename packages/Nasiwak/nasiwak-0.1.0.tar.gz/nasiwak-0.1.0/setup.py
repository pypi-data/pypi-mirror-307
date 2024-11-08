# setup.py
from setuptools import setup, find_packages

setup(
    name="Nasiwak",            # Your package name
    version="0.1.0",             # Initial version
    author="Kushal",
    author_email="Kushalnasiak@outlook.com",
    description="A model that contains all the needs of Nasiwak Company",
    packages=find_packages(),    # Automatically discover all packages in the module
    install_requires=[
        "selenium >= 4.26.0"],         # Dependencies (add here if your code depends on other packages)
    license="MIT",
)