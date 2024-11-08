# Building setup to package 'utl_logger'
import os
from setuptools import setup, find_packages

# Reading README.md as description
readme_path: os.PathLike[str] = os.path.join(os.path.dirname(__file__), "README.md")
with open(file=readme_path, mode="r") as fh:
    long_description = fh.read()
    fh.close()

# Reading requirements.txt for utl_logger
requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
with open(file=requirements_path, mode="r") as f:
    required = f.read().splitlines()
    f.close()

# Setup
setup(
    name="emp_logger",
    version="1.0.0",
    description="""Custom logger with dynamic customizability for all emp-microservices that require a python logger module""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AbdoCherry",
    packages=find_packages(where="src", include=["logger"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    license="MIT",
    url="https://github.com/AbdoCherry/EMP_UTL-S",
)
