from setuptools import setup, find_packages

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pysomo",
    version="0.0.4",
    author="Louis Carl Pepin",
    author_email="lcpepin@louiscarl.com",
    description="A small solid modeling library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/louiscarl/pysomo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
