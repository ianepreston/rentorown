from setuptools import setup, find_packages
from version import find_version

setup(
    name="mortgage",
    author="Ian Preston",
    version=find_version("mortgage", "__init__.py"),
    description="rent or own calculations",
    license="GPL",
    packages=find_packages(),
)
