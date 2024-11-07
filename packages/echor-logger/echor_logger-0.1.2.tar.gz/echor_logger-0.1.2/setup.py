from setuptools import setup, find_packages

setup(
    name="echor-logger",
    version="0.1.2",
    packages=find_packages(),
    description="A simple Python logging utility",
    author="Pradeep",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)