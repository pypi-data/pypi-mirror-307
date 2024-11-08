from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="MySQL-DataBridge",
    version="0.1.0.2",  # Ensure this is a unique version
    author="H-Rasheed",
    author_email="rsm878yourkhan@gmail.com",
    description="A lightweight Python module to simplify MySQL database connections and queries.",
    long_description=long_description,  # Use the variable here
    long_description_content_type="text/markdown",
    url="https://github.com/Manti-Rashee/MySQL-DataBridge",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "mysql-connector-python"
    ],
)
