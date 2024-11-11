import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="logic-ds2",
    version="0.0.3",
    author="Barnas Monteith,LogicDS",
    author_email="barnas@engagescience.org",
    description="LogicDS reasoning-based universal language teaching library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/brn378/logicds",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
)
