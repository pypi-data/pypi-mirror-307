from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pypostfix",
    version="1.0.0",
    author="Alexandre Poggioli",
    author_email="alexandrepoggioli09@gmail.com",
    description="A library for manipulating expressions in both infix and postfix notation (Reverse Polish Notation or RPN)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=" https://github.com/Slinky802/pypostfix",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    entry_points={
        "console_scripts": [
            "pypostfix = pypostfix.cli:main",
        ],
    },
)