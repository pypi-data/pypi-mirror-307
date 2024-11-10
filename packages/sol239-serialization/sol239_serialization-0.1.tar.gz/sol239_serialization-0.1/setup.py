# setup.py
from setuptools import setup, find_packages

setup(
    name="sol239_serialization",  # Ensure this matches your PyPI package name
    version="0.1",
    packages=find_packages(),
    description="A package for serializing and deserializing data",
    author="sol239",
    author_email="239sol239@gmail.com",
    url="https://github.com/sol239/ClassSerialization",
    license="GPLv3",  # Updated to match classifier
    install_requires=[],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",  # Matches the license specified above
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
