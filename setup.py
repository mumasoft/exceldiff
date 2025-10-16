from setuptools import setup, find_packages

setup(
    name="exceldiff",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openpyxl>=3.1.2",
        "click>=8.1.7",
    ],
    entry_points={
        "console_scripts": [
            "exceldiff=exceldiff.cli:main",
        ],
    },
    python_requires=">=3.13",
)
