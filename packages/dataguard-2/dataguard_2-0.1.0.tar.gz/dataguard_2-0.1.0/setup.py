from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
with open("requirements.txt") as f:
    required = f.read().splitlines()
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.1.0"
DESCRIPTION = "Data quality tools"
LONG_DESCRIPTION = "A package that allows to moniter data quality"

# Setting up
setup(
    name="dataguard_2",
    version=VERSION,
    author="Anirudha Bidave",
    author_email="anirudha.b@sigmoidanalytics.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        required,
    ],
    package_data={
        "": ["requirements.txt"],  # include requirements.txt in the package
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
