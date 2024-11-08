# mypypkg/setup.py

from setuptools import setup, find_packages

setup(
    name="gagan_mypkg",  # Package name
    version="0.1.1",     # Version
    packages=find_packages(),
    description="A simple math package with basic operations",
    long_description=open("README.md").read(),  # Use the README file for description
    long_description_content_type="text/markdown",
    author="Gagandeep",
    author_email="gagandeep-singh@cssoftsolutions.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
