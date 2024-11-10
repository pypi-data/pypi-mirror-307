from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name="isNumberFour",
    version="0.1.2",
    description="A Python library to Check whether the value is Number 4 or Not",
    long_description=description,
    long_description_content_type="text/markdown",
    author="Yajith Vishwa",
    author_email="yajithvishwa2001@example.com",
    url="https://github.com/YajithVishwa/isNumberFour",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
