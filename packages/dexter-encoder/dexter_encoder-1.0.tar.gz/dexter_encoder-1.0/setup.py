from setuptools import setup, find_packages
import pathlib  # Import pathlib to read the README file

# Package meta-data
NAME = "dexter-encoder"
VERSION = "1.0"
AUTHOR = "Ethan Fraser"
AUTHOR_EMAIL = "ethanprime.c137@mail.com"
DESCRIPTION = "A simple dynamic encoder and decoder with random shifts."
URL = "https://github.com/Brownpanda29/dexter"
REQUIRES_PYTHON = ">=3.6"
KEYWORDS = ["python", "encoding", "decoding", "shellcode", "security"]

# Read the contents of README.md
README = (pathlib.Path(__file__).parent / "README.md").read_text()

# Package setup
setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=README,  # Use README.md for the PyPI long description
    long_description_content_type="text/markdown",  # Specify Markdown format
    url=URL,
    packages=find_packages(),
    python_requires=REQUIRES_PYTHON,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=KEYWORDS,
)
