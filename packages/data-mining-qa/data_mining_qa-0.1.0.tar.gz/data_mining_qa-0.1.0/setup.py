# setup.py
from setuptools import setup, find_packages

setup(
    name="data_mining_qa",  # Name of your package
    version="0.1.0",  # Your current version
    description="A simple library providing answers to common data mining questions.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    url="",  # Leave empty or set it to your project homepage if you have one
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
