from setuptools import setup

# store readme.md files
with open("README.md", "r") as fh:
    long_description = fh.read()
# read the requirements
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setup(
    name="FoundationDesign",
    packages=["FoundationDesign"],
    version="0.1.2",
    author="Kunle Yusuf",
    author_email="kunleyusuf858@gmail.com",
    description="A python module for structural analysis and design of different foundation types in accordance to the Eurocodes",
    url="https://github.com/kunle009/FoundationDesign",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
)
