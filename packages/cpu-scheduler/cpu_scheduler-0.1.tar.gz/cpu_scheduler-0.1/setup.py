# setup.py
from setuptools import setup, find_packages

setup(
    name="cpu-scheduler",
    version="0.1",
    description="A Python library for CPU scheduling algorithms",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nitish",
    author_email="nitishnaik2022@gmail.com",
    url="https://github.com/Nitish-Naik/schedulipy.git", # GitHub repo or other URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
