# setup.py

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sqqueue",  # Replace with your desired package name
    version="0.1.0",
    author="James AMD",
    author_email="***@example.com",
    description="A SQLite-based persistent queue implementation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaymd/sqqueue",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "statsd>=3.3.0; extra == 'statsd'",
    ],
    extras_require={
        "dev": [
            "pre-commit",
            "pytest",
            "pytest-mock",
            "ruff",
            "black",
            "isort",
            "twine",
            "isort",
            "statsd",
        ],
    },
    include_package_data=True,
)
