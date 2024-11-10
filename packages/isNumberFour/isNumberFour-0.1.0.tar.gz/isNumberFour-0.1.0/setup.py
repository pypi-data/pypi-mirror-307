from setuptools import setup, find_packages

setup(
    name="isNumberFour",
    version="0.1.0",
    description="A Python library to Check whether the value is Number 4 or Not",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Yajith Vishwa",
    author_email="yajithvishwa2001@example.com",
    url="https://github.com/YajithVishwa/isNumberFour",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
)
