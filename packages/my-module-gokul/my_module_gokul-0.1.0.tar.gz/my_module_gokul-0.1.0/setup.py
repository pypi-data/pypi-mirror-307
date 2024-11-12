# setup.py

from setuptools import setup, find_packages

setup(
    name="my_module_gokul",  # The name of your module on PyPI
    version="0.1.0",
    author="Gokul",
    author_email="gokult.22aid@kongu.edu",
    description="A simple Python module that prints 'Hello, World!'",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),  # Automatically find sub-packages like "my_module"
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
