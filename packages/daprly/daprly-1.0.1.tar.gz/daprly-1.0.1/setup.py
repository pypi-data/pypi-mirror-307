from setuptools import setup, find_packages

# metadata...
name = "daprly"
description = (
    "A simple Dapr Python SDK wrapper util."
)
author = "Simon Stipcich"
author_email = "stipcich.simon@gmail.com"
url = "https://github.com/stiproot/daprly"
license = "MIT"
keywords = ["python", "package", "dapr", "beta"]
version = "1.0.1"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# dependencies...
install_requires = [
    "dapr>=1.13.0a,<1.14.0",
]

# setup...
setup(
    name=name,
    version=version,
    packages=find_packages(where="src"),
    package_dir={"daprly": "src/daprly"},
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    keywords=keywords,
    install_requires=install_requires,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
    ],
)
