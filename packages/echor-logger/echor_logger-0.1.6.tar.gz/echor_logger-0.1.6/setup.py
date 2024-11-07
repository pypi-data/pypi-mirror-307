from setuptools import setup, find_packages

setup(
    name="echor-logger",
    version="0.1.6",
    packages=find_packages(),
    description="A simple Python logging utility",
    author="Pradeep",
    install_requires=[
        "python-dotenv",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
