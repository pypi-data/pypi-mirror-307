# setup.py
from setuptools import setup, find_packages

setup(
    name="calpi",
    version="1.1",
    packages=find_packages(),
    author="PandaDev.py",  # Your alias here
    author_email="None :)",  # Or leave it blank if you prefer
    description="Calculate Pi easily with the Calpi library",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FreezingPanda/calpi_python_lib",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
